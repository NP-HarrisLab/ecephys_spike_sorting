import json
import os
import sys
import time
from pathlib import Path

import numpy as np

from ecephys_spike_sorting.common.SGLXMetaToCoords import MetaToCoords
from ecephys_spike_sorting.common.utils import write_probe_json
from ecephys_spike_sorting.modules.depth_estimation.depth_estimation import (
    compute_channel_offsets,
    find_surface_channel,
)
from ecephys_spike_sorting.modules.utils import ObjectEncoder

from ._schemas import DepthSchema


def run_depth_estimation(args):

    print("ecephys spike sorting: depth estimation module\n")

    start = time.time()

    numChannels = args["ephys_params"]["num_channels"]

    rawDataAp = np.memmap(args["ephys_params"]["ap_band_file"], dtype="int16", mode="r")
    dataAp = np.reshape(rawDataAp, (int(rawDataAp.size / numChannels), numChannels))

    rawDataLfp = np.memmap(
        args["ephys_params"]["lfp_band_file"], dtype="int16", mode="r"
    )
    dataLfp = np.reshape(rawDataLfp, (int(rawDataLfp.size / numChannels), numChannels))

    metaName, binExt = os.path.splitext(args["ephys_params"]["ap_band_file"])
    metaFullPath = Path(metaName + ".meta")

    [xCoord, yCoord, shankInd, connected] = MetaToCoords(
        metaFullPath,
        -1,
        badChan=np.zeros((0), dtype="int"),
        destFullPath="",
        showPlot=False,
    )

    print("Computing surface channel...")

    info_lfp = find_surface_channel(
        dataLfp,
        args["ephys_params"],
        args["depth_estimation_params"],
        xCoord,
        yCoord,
        shankInd,
    )

    write_probe_json(
        args["common_files"]["probe_json"],
        info_lfp["surface_y"],
        info_lfp["air_y"],
        np.squeeze(yCoord),
        np.squeeze(xCoord),
        np.squeeze(shankInd),
    )

    execution_time = time.time() - start

    print("total time: " + str(np.around(execution_time, 2)) + " seconds")
    print()

    return {
        "surface_channel": info_lfp["surface_y"],
        "air_channel": info_lfp["air_y"],
        "probe_json": args["common_files"]["probe_json"],
        "execution_time": execution_time,
    }  # output manifest


def main():
    """Main entry point:"""
    input_json_index = sys.argv.index("--input_json") + 1
    with open(sys.argv[input_json_index]) as f:
        input_json = json.load(f)
    output_json_index = sys.argv.index("--output_json") + 1
    output_json = sys.argv[output_json_index]
    args = DepthSchema().load({"input": input_json, "output": {}})

    output = run_depth_estimation(args["input"])

    output.update({"input_parameters": args["input"]})
    with open(output_json, "w") as f:
        json.dump(output, f, indent=2, cls=ObjectEncoder)


if __name__ == "__main__":
    main()
