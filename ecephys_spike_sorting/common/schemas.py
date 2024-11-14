from marshmallow import Schema
from marshmallow.fields import Bool, Float, Int, String

from ecephys_spike_sorting.modules.schema_fields import InputDir, NumpyArray, OutputDir


class EphysParams(Schema):
    sample_rate = Float(
        required=False,
        missing=30000.0,
        help="Sample rate of Neuropixels AP band continuous data",
    )
    lfp_sample_rate = Float(
        require=False,
        missing=2500.0,
        help="Sample rate of Neuropixels LFP band continuous data",
    )
    bit_volts = Float(
        required=False,
        missing=0.195,
        help="Scalar required to convert int16 values into microvolts",
    )
    num_channels = Int(
        required=False,
        missing=384,
        help="Total number of channels in binary data files",
    )
    reference_channels = NumpyArray(
        required=False,
        missing=[36, 75, 112, 151, 188, 227, 264, 303, 340, 379],
        help="Reference channels on Neuropixels probe (numbering starts at 0)",
    )
    template_zero_padding = Int(
        required=False, missing=21, help="Zero-padding on templates output by Kilosort"
    )
    vertical_site_spacing = Float(
        required=False, missing=20e-6, help="Vertical site spacing in meters"
    )
    probe_type = String(required=False, missing="NP1", help="3A, 3B2, NP1")
    lfp_band_file = String(required=False, help="Location of LFP band binary file")
    ap_band_file = String(required=False, help="Location of AP band binary file")
    reorder_lfp_channels = Bool(
        required=False,
        missing=True,
        help="Should we fix the ordering of LFP channels (necessary for 3a probes following extract_from_npx modules)",
    )
    cluster_group_file_name = String(required=False, missing="cluster_group.tsv")


class Directories(Schema):

    ecephys_directory = InputDir(
        help="Location of the ecephys_spike_sorting directory containing modules directory"
    )
    npx_directory = InputDir(help="Location of raw neuropixels binary files")
    kilosort_output_directory = OutputDir(help="Location of Kilosort output files")
    extracted_data_directory = OutputDir(help="Location for NPX/CatGT processed files")
    kilosort_output_tmp = OutputDir(help="Location for temporary KS output")


class CommonFiles(Schema):

    probe_json = String(help="Location of probe JSON file")
    settings_json = String(
        help="Location of settings JSON written by extract_from_npx module"
    )


class WaveformMetricsFile(Schema):
    waveform_metrics_file = String(help="Location of waveform metrics CSV")


class ClusterMetricsFile(Schema):
    cluster_metrics_file = String(help="Location of cluster metrics CSV")
