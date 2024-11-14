from marshmallow import INCLUDE, Schema
from marshmallow.fields import Bool, Float, Int, Nested, String

from ecephys_spike_sorting.modules.schema_fields import InputDir

from ...common.schemas import (
    ClusterMetricsFile,
    Directories,
    EphysParams,
    WaveformMetricsFile,
)


class MeanWaveformParams(Schema):
    class Meta:
        unknown = INCLUDE

    samples_per_spike = Int(
        required=False, missing=82, help="Number of samples to extract for each spike"
    )
    pre_samples = Int(
        required=False,
        missing=20,
        help="Number of samples between start of spike and the peak",
    )
    num_epochs = Int(
        required=False, missing=1, help="Number of epochs to compute mean waveforms"
    )
    nAP = Int(required=False, missing=384, help="Number AP channels in saved file")
    spikes_per_epoch = Int(
        require=False, missing=100, help="Max number of spikes per epoch"
    )
    upsampling_factor = Float(
        require=False,
        missing=200 / 82,
        help="Upsampling factor for calculating waveform metrics",
    )
    spread_threshold = Float(
        require=False,
        missing=0.12,
        help="Threshold for computing channel spread of 2D waveform",
    )
    site_range = Int(
        require=False, missing=16, help="Number of sites to use for 2D waveform metrics"
    )
    cWaves_path = InputDir(
        require=False, help="directory containing the TPrime executable."
    )
    use_C_Waves = Bool(
        require=False,
        missing=False,
        help="Use faster C routine to calculate mean waveforms",
    )
    snr_radius = Int(
        require=False,
        missing=8,
        help="disk radius (chans) about pk-chan for snr calculation in C_waves",
    )
    snr_radius_um = Int(
        require=False,
        missing=8,
        help="disk radius (um) about pk-chan for snr calculation in C_waves",
    )
    mean_waveforms_file = String(
        required=False, help="Path to mean waveforms file (.npy)"
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    waveform_metrics = Nested(WaveformMetricsFile)
    mean_waveform_params = Nested(MeanWaveformParams)
    cluster_metrics = Nested(ClusterMetricsFile)
    ephys_params = Nested(EphysParams)
    directories = Nested(Directories)


class OutputSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input_parameters = Nested(
        InputParameters,
        description=("Input parameters the module " "was run with"),
        required=False,
    )


class OutputParameters(OutputSchema):
    class Meta:
        unknown = INCLUDE

    execution_time = Float()
    mean_waveforms_file = String()


class MeanWaveformSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
