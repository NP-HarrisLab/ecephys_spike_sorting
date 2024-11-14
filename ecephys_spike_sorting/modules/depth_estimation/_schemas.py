from marshmallow import INCLUDE, Schema
from marshmallow.fields import Bool, Float, Int, Nested, String

from ecephys_spike_sorting.modules.schema_fields import NumpyArray, OutputFile

from ...common.schemas import CommonFiles, Directories, EphysParams


class DepthEstimationParams(Schema):
    class Meta:
        unknown = INCLUDE

    hi_noise_thresh = Float(
        required=False, missing=50.0, help="Max RMS noise for including channels"
    )
    lo_noise_thresh = Float(
        required=False, missing=3.0, help="Min RMS noise for including channels"
    )

    save_figure = Bool(required=False, missing=True)
    figure_location = OutputFile(required=False, missing=None)

    smoothing_amount = Int(
        required=False,
        missing=5,
        help="Gaussian smoothing parameter to reduce channel-to-channel noise",
    )
    power_thresh = Float(
        required=False,
        missing=2.5,
        help="Ignore threshold crossings if power is above this level (indicates channels are in the brain)",
    )
    diff_thresh = Float(
        required=False,
        missing=-0.07,
        help="Threshold to detect large increases is power at brain surface",
    )
    freq_range = NumpyArray(
        required=False,
        missing=[0, 10],
        help="Frequency band for detecting power increases",
    )
    max_freq = Int(required=False, missing=150, help="Maximum frequency to plot")
    saline_range_um = NumpyArray(
        required=False,
        missing=[3700, 3800],
        help="Y range assume to be out of brain, but in saline",
    )
    n_passes = Int(
        required=False,
        missing=10,
        help="Number of times to compute offset and surface channel",
    )
    skip_s_per_pass = Int(
        required=False,
        missing=5,
        help="Number of seconds between data chunks used on each pass",
    )  # missing=100
    start_time = Float(
        required=False,
        missing=0,
        help="First time (in seconds) for computing median offset",
    )
    time_interval = Float(
        required=False, missing=5, help="Number of seconds for computing median offset"
    )

    nfft = Int(required=False, missing=4096, help="Length of FFT used for calculations")

    air_gap_um = Int(
        required=False, missing=1000, help="Approximate um between brain surface and air"
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    depth_estimation_params = Nested(DepthEstimationParams)

    ephys_params = Nested(EphysParams)
    directories = Nested(Directories)
    common_files = Nested(CommonFiles)


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

    surface_channel = Int()
    air_channel = Int()
    probe_json = String()
    execution_time = Float()


class DepthSchema(Schema):
    class Meta:
        unknown = INCLUDE

    schema_type = Nested(InputParameters, required=True)
    output_schema_type = Nested(OutputParameters, required=True)
