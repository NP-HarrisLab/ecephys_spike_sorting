from marshmallow import INCLUDE, Schema
from marshmallow.fields import Bool, Float, Int, Nested, String

from ...common.schemas import CommonFiles, Directories, EphysParams


class ks4_params(Schema):
    class Meta:
        unknown = INCLUDE

    Th_universal = Float(
        required=False, missing=9, help="threshold for creating templates"
    )
    Th_learned = Float(
        required=False, missing=8, help="threshold for creating templates"
    )
    Th_single_ch = Float(
        required=False,
        missing=8,
        help="threshold crossings for pre-clustering (in PCA projection space)",
    )
    duplicate_spike_ms = Float(
        required=False,
        missing=0.25,
        help="Number of bins for which subsequent spikes from the same cluster are assumed to be artifacts. A value of 0 disables this step.",
    )
    nblocks = Int(
        required=False,
        missing=5,
        help="number of blocks used to segment the probe when tracking drift, 0 == do not track, 1 == rigid, > 1 == non-rigid",
    )
    sig_interp = Float(
        required=True,
        missing=20.0,
        help="sigma for the Gaussian interpolation in drift correction um)",
    )
    whitening_range = Int(
        required=False,
        missing=32,
        help="number of channels to use for whitening each channel",
    )
    min_template_size = Float(
        required=False,
        missing=10,
        help="Width in um of Gaussian envelope for template weight",
    )
    template_sizes = Int(
        required=False,
        missing=5,
        help="number of template sizes, multiples of min_template size",
    )
    templates_from_data = Bool(
        required=False, missing=True, help="set to True to extract templates from data"
    )
    tmin = Float(required=False, missing=0, help="time in sec to start processing")
    tmax = Float(
        required=False,
        missing=-1,
        help="time in sec to end processing; if < 0, set to inf ",
    )
    nearest_chans = Int(
        required=False,
        missing=10,
        help="Number of nearest channels to consider when finding local maxima during spike detection.",
    )
    nearest_templates = Int(
        required=False,
        missing=100,
        help="Number of nearest spike template locations to consider when finding local maxima during spike detection.",
    )
    ccg_threshold = Float(
        required=False,
        missing=0.25,
        help="Fraction of refractory period violations that are allowed in the CCG compared to baseline; used to perform splits and merges. ",
    )
    acg_threshold = Float(
        required=False,
        missing=0.20,
        help='Fraction of refractory period violations that are allowed in the ACG compared to baseline; used to assign "good" units. ',
    )
    template_seed = Int(
        required=False,
        missing=0,
        help="seed to pick which batches are used for finding universal templates",
    )
    cluster_seed = Int(required=False, missing=0, help="start seed for clustering")


class KS4HelperParameters(Schema):
    class Meta:
        unknown = INCLUDE

    do_CAR = Bool(
        required=False,
        missing=True,
        help="set to True to perform common average referencing (median subtraction)",
    )
    save_extra_vars = Bool(
        required=False,
        missing=False,
        help="If true, save Wall and pc features in save_to_phy ",
    )
    ks_make_copy = Bool(
        required=False,
        missing=False,
        help="If true, make a copy of the original KS output",
    )
    save_preprocessed_copy = Bool(
        required=False,
        missing=False,
        help="If true, make a copy of the prprocessed data",
    )
    doFilter = Int(
        required=False, missing=0, help="filter if = 1, skip bp filtering if = 0"
    )
    fproc = String(
        required=False,
        missing="D:\kilosort_datatemp\temp_wh.dat",
        help="Processed data file on a fast ssd",
    )
    fshigh = Float(
        required=False, allow_none=True, missing=300, help="high pass filter frequency"
    )
    fslow = Float(
        required=False, allow_none=True, missing=10000, help="low pass filter frequency"
    )
    ks4_params = Nested(
        ks4_params,
        required=True,
        help="Parameters used to auto-generate a Kilosort config file",
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    ks4_helper_params = Nested(KS4HelperParameters)
    directories = Nested(Directories)
    ephys_params = Nested(EphysParams)
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

    message = String()
    execution_time = Float()


class Ks4Schema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
