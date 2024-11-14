import json
import os
import pathlib
import sys
import time

import numpy as np
import pandas as pd

from ecephys_spike_sorting.modules.utils import ObjectEncoder

from ...common.utils import getFileVersion, load_kilosort_data
from ._schemas import QualityMetricsSchema
from .ibl_metrics import calculate_ibl_metrics
from .metrics import calculate_metrics


def calculate_quality_metrics(args):

    print("ecephys spike sorting: quality metrics module")

    start = time.time()

    include_pcs = args["quality_metrics_params"]["include_pcs"]

    # make usre we can write an output file

    output_file_args = args["cluster_metrics"]["cluster_metrics_file"]

    output_file, metrics_version = getFileVersion(output_file_args)

    print("kilosort_output_dir: ")
    print(args["directories"]["kilosort_output_directory"])
    print("Loading data...")

    try:
        if include_pcs:
            (
                spike_times,
                spike_clusters,
                spike_templates,
                amplitudes,
                templates,
                channel_map,
                channel_pos,
                clusterIDs,
                cluster_quality,
                cluster_amplitude,
                pc_features,
                pc_feature_ind,
                template_features,
            ) = load_kilosort_data(
                args["directories"]["kilosort_output_directory"],
                args["ephys_params"]["sample_rate"],
                use_master_clock=False,
                include_pcs=include_pcs,
            )
        else:
            (
                spike_times,
                spike_clusters,
                spike_templates,
                amplitudes,
                templates,
                channel_map,
                channel_pos,
                clusterIDs,
                cluster_quality,
                cluster_amplitude,
            ) = load_kilosort_data(
                args["directories"]["kilosort_output_directory"],
                args["ephys_params"]["sample_rate"],
                use_master_clock=False,
                include_pcs=include_pcs,
            )
            pc_features = []
            pc_feature_ind = []

        metrics = calculate_metrics(
            spike_times,
            spike_clusters,
            spike_templates,
            amplitudes,
            channel_map,
            channel_pos,
            templates,
            pc_features,
            pc_feature_ind,
            args["quality_metrics_params"],
        )
        if args["quality_metrics_params"]["include_ibl"]:
            ibl_metrics = calculate_ibl_metrics(
                spike_times,
                spike_clusters,
                amplitudes,
                args["quality_metrics_params"],
                args["ephys_params"]["sample_rate"],
            )

    except FileNotFoundError:

        execution_time = time.time() - start

        print(" Files not available.")

        return {"execution_time": execution_time, "quality_metrics_output_file": None}

    if args["quality_metrics_params"]["include_ibl"]:
        # merge allen and ibl metrics
        metrics = metrics.merge(
            ibl_metrics, on="cluster_id", suffixes=("_quality_metrics", "_ibl")
        )

    # build name for waveform_metrics file with matched version
    wm_args = args["waveform_metrics"]["waveform_metrics_file"]
    if metrics_version == 0:
        wm = wm_args
    else:
        # buld name for waveform metrics file with matched version
        wm = os.path.join(
            pathlib.Path(wm_args).parent,
            pathlib.Path(wm_args).stem + "_" + repr(metrics_version) + ".csv",
        )
    if os.path.exists(wm):
        metrics = metrics.merge(
            pd.read_csv(wm, index_col=0),
            on="cluster_id",
            suffixes=("_quality_metrics", "_waveform_metrics"),
        )

    print("Saving data...")

    metrics.to_csv(output_file, index=False)

    execution_time = time.time() - start

    print("total time: " + str(np.around(execution_time, 2)) + " seconds")
    print()

    return {
        "execution_time": execution_time,
        "quality_metrics_output_file": output_file,
    }  # output manifest


def main():
    """Main entry point:"""
    input_json_index = sys.argv.index("--input_json") + 1
    with open(sys.argv[input_json_index]) as f:
        input_json = json.load(f)
    output_json_index = sys.argv.index("--output_json") + 1
    output_json = sys.argv[output_json_index]
    args = QualityMetricsSchema().load({"input": input_json, "output": {}})

    output = calculate_quality_metrics(args["input"])

    output.update({"input_parameters": args["input"]})
    with open(output_json, "w") as f:
        json.dump(output, f, indent=2, cls=ObjectEncoder)


if __name__ == "__main__":
    main()
