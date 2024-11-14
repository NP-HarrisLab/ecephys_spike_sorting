import json
import logging
import subprocess
import sys
import time

import numpy as np

from ecephys_spike_sorting.modules.utils import ObjectEncoder

from ...common.utils import get_repo_commit_date_and_hash, read_probe_json
from ._schemas import MedianSubtractionSchema


def run_median_subtraction(args):

    print("ecephys spike sorting: median subtraction module")

    commit_date, commit_hash = get_repo_commit_date_and_hash(
        args["median_subtraction_params"]["median_subtraction_repo"]
    )

    mask, offset, scaling, surface_channel, air_channel = read_probe_json(
        args["common_files"]["probe_json"]
    )

    logging.info("Running median subtraction")

    start = time.time()

    subprocess.check_call(
        [
            args["median_subtraction_params"]["median_subtraction_executable"],
            args["common_files"]["probe_json"],
            args["ephys_params"]["ap_band_file"],
            str(int(air_channel)),
        ]
    )

    execution_time = time.time() - start

    print("total time: " + str(np.around(execution_time, 2)) + " seconds")
    print()

    return {
        "median_subtraction_execution_time": execution_time,
        "median_subtraction_commit_date": commit_date,
        "median_subtraction_commit_hash": commit_hash,
    }  # output manifest} # output manifest


def main():
    """Main entry point:"""
    input_json_index = sys.argv.index("--input_json") + 1
    with open(sys.argv[input_json_index]) as f:
        input_json = json.load(f)
    output_json_index = sys.argv.index("--output_json") + 1
    output_json = sys.argv[output_json_index]
    args = MedianSubtractionSchema().load({"input": input_json, "output": {}})

    output = run_median_subtraction(args["input"])

    output.update({"input_parameters": args["input"]})
    with open(output_json, "w") as f:
        json.dump(output, f, indent=2, cls=ObjectEncoder)


if __name__ == "__main__":
    main()
