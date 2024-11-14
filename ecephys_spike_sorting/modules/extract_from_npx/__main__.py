import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np

from ecephys_spike_sorting.modules.utils import ObjectEncoder

from ...common.utils import get_repo_commit_date_and_hash
from ._schemas import NpxSchema


def run_npx_extractor(args):

    print("ecephys spike sorting: npx extractor module")

    start = time.time()

    commit_date, commit_hash = get_repo_commit_date_and_hash(
        args["extract_from_npx_params"]["npx_extractor_repo"]
    )

    extracted_data_drive, directory = os.path.splitdrive(
        args["directories"]["extracted_data_directory"]
    )

    _, _, free = shutil.disk_usage(extracted_data_drive)

    filesize = os.path.getsize(args["extract_from_npx_params"]["npx_directory"])

    assert free > filesize * 2

    if not os.path.exists(args["directories"]["extracted_data_directory"]):
        os.mkdir(args["directories"]["extracted_data_directory"])

    subprocess.check_call(
        [
            args["extract_from_npx_params"]["npx_extractor_executable"],
            args["extract_from_npx_params"]["npx_directory"],
            args["directories"]["extracted_data_directory"],
        ]
    )

    execution_time = time.time() - start

    # settings_json = create_settings_json(args['extract_from_npx_params']['settings_xml'])

    # with io.open(args['common_files']['settings_json'], 'w', encoding='utf-8') as f:
    #    f.write(json.dumps(settings_json, ensure_ascii=False, sort_keys=True, indent=4))

    print("total time: " + str(np.around(execution_time, 2)) + " seconds")
    print()

    return {
        "execution_time": execution_time,
        "npx_extractor_commit_date": commit_date,
        "npx_extractor_commit_hash": commit_hash,
    }  # output manifest


def main():
    """Main entry point:"""
    input_json_index = sys.argv.index("--input_json") + 1
    with open(sys.argv[input_json_index]) as f:
        input_json = json.load(f)
    output_json_index = sys.argv.index("--output_json") + 1
    output_json = sys.argv[output_json_index]
    args = NpxSchema().load({"input": input_json, "output": {}})

    output = run_npx_extractor(args["input"])

    output.update({"input_parameters": args["input"]})
    with open(output_json, "w") as f:
        json.dump(output, f, indent=2, cls=ObjectEncoder)


if __name__ == "__main__":
    main()
