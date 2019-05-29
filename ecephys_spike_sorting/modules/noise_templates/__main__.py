from argschema import ArgSchemaParser
import os
import logging
import time

from .id_noise_templates import id_noise_templates_rf

from ...common.utils import write_cluster_group_tsv, load_kilosort_data


def classify_noise_templates(args):

    logging.info('Running noise template identification')
    
    start = time.time()

    spike_times, spike_clusters, amplitudes, templates, channel_map, cluster_ids, cluster_quality = \
            load_kilosort_data(args['directories']['kilosort_output_directory'], \
                args['ephys_params']['sample_rate'], \
                convert_to_seconds = True)
    
    #cluster_ids, is_noise = id_noise_templates(spike_times, spike_clusters, \
    #    cluster_ids, templates, \
    #    args['noise_waveform_params'])

    cluster_ids, is_noise = id_noise_templates_rf(spike_times, spike_clusters, \
        cluster_ids, templates, \
        args['noise_waveform_params'])

    write_cluster_group_tsv(cluster_ids, is_noise, args['directories']['kilosort_output_directory'])
    
    print(is_noise)

    execution_time = time.time() - start
    
    return {"execution_time" : execution_time} # output manifest


def main():

    from ._schemas import InputParameters, OutputParameters

    mod = ArgSchemaParser(schema_type=InputParameters,
                          output_schema_type=OutputParameters)

    output = classify_noise_templates(mod.args)

    output.update({"input_parameters": mod.args})
    if "output_json" in mod.args:
        mod.output(output, indent=2)
    else:
        print(mod.get_output_json(output))


if __name__ == "__main__":
    main()