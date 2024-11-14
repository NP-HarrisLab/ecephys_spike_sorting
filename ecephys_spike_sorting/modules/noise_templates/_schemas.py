from marshmallow import INCLUDE, Schema
from marshmallow.fields import Boolean, Float, Int, Nested, String

from ...common.schemas import Directories, EphysParams


class NoiseWaveformParams(Schema):
    class Meta:
        unknown = INCLUDE

    classifier_path = String(
        required=True, help="Path to pre-trained waveform classifier"
    )

    smoothed_template_amplitude_threshold = Float(
        missing=0.2, help="Fraction of max amplitude for calculating spread"
    )
    template_amplitude_threshold = Float(
        missing=0.2, help="Fraction of max amplitude for calculating spread"
    )
    smoothed_template_filter_width = Int(
        missing=2, help="Smoothing window for calculating spread"
    )
    min_spread_threshold = Int(
        missing=2,
        help="Minimum number of channels for a waveform to be considered good",
    )
    mid_spread_threshold = Int(
        missing=16, help="Over this channel spread, waveform shape must be considered"
    )
    max_spread_threshold = Int(
        missing=25, help="Maximum channel spread for a good unit"
    )
    smoothed_template_filter_width_um = Int(
        missing=15, help="Smoothing window for calculating spread"
    )
    min_spread_threshold_um = Int(
        missing=10, help="Minimum spatial spread of a waveform to be considered good"
    )
    mid_spread_threshold_um = Int(
        missing=50, help="Over this channel spread, waveform shape must be considered"
    )
    max_spread_threshold_um = Int(
        missing=300, help="Maximum channel spread for a good unit"
    )

    channel_amplitude_thresh = Float(
        missing=0.3,
        help="Fraction of max amplitude for considering channels in spatial peak detection",
    )
    peak_height_thresh = Float(
        missing=0.2, help="Minimum height for spatial peak detection"
    )
    peak_prominence_thresh = Float(
        missing=0.2, help="Minimum prominence for spatial peak detection"
    )
    peak_channel_range = Int(
        missing=24, help="Range of channels for detecting spatial peaks"
    )
    peak_channel_range_um = Int(
        missing=150, help="Range of in um to check for spatial peaks"
    )
    peak_locs_std_thresh = Float(
        missing=3.5, help="Maximum standard deviation of peak locations for good units"
    )

    min_temporal_peak_location = Int(
        missing=10, help="Minimum peak index for good unit"
    )
    max_temporal_peak_location = Int(
        missing=30, help="Maximum peak index for good unit"
    )

    template_shape_channel_range = Int(
        missing=12, help="Range of channels for checking template shape"
    )
    wavelet_index = Int(
        missing=2, help="Wavelet index for noise template shape detection"
    )
    min_wavelet_peak_height = Float(
        missing=0.0, help="Minimum wavelet peak height for good units"
    )
    min_wavelet_peak_loc = Int(
        missing=15, help="Minimum wavelet peak location for good units"
    )
    max_wavelet_peak_loc = Int(
        missing=25, help="Maximum wavelet peak location for good units"
    )

    multiprocessing_worker_count = Int(
        missing=4, help="Number of workers to use for spatial peak calculation"
    )
    use_random_forest = Boolean(
        missing=False, help="set to false to use heuristic  noise id"
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    noise_waveform_params = Nested(NoiseWaveformParams)
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


class NoiseTemplateSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
