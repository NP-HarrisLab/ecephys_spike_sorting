import json
import sys
import time

import numpy as np

from ecephys_spike_sorting.modules.utils import ObjectEncoder

from ...common.utils import load_kilosort_data, write_cluster_group_tsv
from ._schemas import NoiseTemplateSchema
from .id_noise_templates import id_noise_templates, id_noise_templates_rf


def classify_noise_templates(args):

    print("ecephys spike sorting: noise templates module")

    start = time.time()

    (
        spike_times,
        spike_clusters,
        spike_templates,
        amplitudes,
        templates,
        channel_map,
        channel_pos,
        cluster_ids,
        cluster_quality,
        cluster_amplitude,
    ) = load_kilosort_data(
        args["directories"]["kilosort_output_directory"],
        args["ephys_params"]["sample_rate"],
        convert_to_seconds=True,
    )

    if args["noise_waveform_params"]["use_random_forest"]:
        # use random forest classifier
        cluster_ids, is_noise = id_noise_templates_rf(
            spike_times,
            spike_clusters,
            cluster_ids,
            templates,
            args["noise_waveform_params"],
        )
    else:
        # use heuristics to identify templates that look like noise
        cluster_ids, is_noise = id_noise_templates(
            cluster_ids, templates, channel_pos, args["noise_waveform_params"]
        )

    mapping = {False: "good", True: "noise"}
    labels = [mapping[value] for value in is_noise]

    write_cluster_group_tsv(
        cluster_ids,
        labels,
        args["directories"]["kilosort_output_directory"],
        args["ephys_params"]["cluster_group_file_name"],
    )

    execution_time = time.time() - start

    print("total time: " + str(np.around(execution_time, 2)) + " seconds")
    print()

    return {"execution_time": execution_time}  # output manifest


def main():
    """Main entry point:"""
    input_json_index = sys.argv.index("--input_json") + 1
    with open(sys.argv[input_json_index]) as f:
        input_json = json.load(f)
    output_json_index = sys.argv.index("--output_json") + 1
    output_json = sys.argv[output_json_index]
    args = NoiseTemplateSchema().load({"input": input_json, "output": {}})

    output = classify_noise_templates(args["input"])

    output.update({"input_parameters": args["input"]})
    with open(output_json, "w") as f:
        json.dump(output, f, indent=2, cls=ObjectEncoder)


if __name__ == "__main__":
    main()
