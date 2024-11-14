from marshmallow import INCLUDE, Schema
from marshmallow.fields import Bool, Float, Int, Nested, String

from ecephys_spike_sorting.modules.schema_fields import InputDir, NumpyArray

from ...common.schemas import CommonFiles, Directories, EphysParams


class KilosortParameters(Schema):
    class Meta:
        unknown = INCLUDE

    Nfilt = Int(required=False, missing=1024)
    Threshold = String(required=False, missing="[4, 10, 10]")
    lam = String(required=False, missing="[5, 20, 20]")
    IntitalizeTh = Int(required=False, missing=-4)
    InitializeNfilt = Int(required=False, missing=10000)


class Kilosort2Parameters(Schema):
    class Meta:
        unknown = INCLUDE

    trange = String(
        required=False, missing="[0 Inf]", help="Time range in seconds to process"
    )
    fproc = String(
        required=False,
        missing="fullfile('D:\kilosort_datatemp', 'temp_wh.dat')",
        help="Processed data file on a fast ssd",
    )

    KSver = String(
        required=False,
        missing="2.5",
        help="kilsort version: 2.0 (tracking) or 2.5(data shift correction)",
    )
    remDup = Int(required=False, missing=0, help="KS2 remove duplicates")
    finalSplits = Int(required=False, missing=1, help="KS2 final splits by SVD")
    labelGood = Int(required=False, missing=1, help="KS2 noise cluster detection")
    saveRez = Int(required=False, missing=1, help="KS2 save rez.mat file")
    copy_fproc = Int(
        required=False, missing=1, help="Copy processed binary to output directory"
    )

    chanMap = String(
        required=False, missing="'chanMap.mat'", help="path to channel map .mat file"
    )
    doFilter = Int(
        required=False,
        missing=1,
        help="filter if = 1, skip bp filetering and CAR if = 0",
    )
    fshigh = Int(required=False, missing=150, help="frequency for high pass filtering")
    minfr_goodchannels = Float(
        required=False,
        missing=0.1,
        help='minimum firing rate on a "good" channel (0 to skip)',
    )
    Th = String(
        required=False, missing="[10 4]", help="threshold (last pass can be lower"
    )
    lam = Int(
        required=False,
        missing=10,
        help="how important is the amplitude penalty (like in Kilosort1, 0 means not used, 10 is average, 50 is a lot)",
    )
    AUCsplit = Float(
        required=False,
        missing=0.9,
        help="splitting a cluster at the end requires at least this much isolation for each sub-cluster (max = 1)",
    )
    minFR = Float(required=False, missing=1 / 50.0, help="minimum spike rate (Hz)")
    momentum = String(
        required=False,
        missing="[20 400]",
        help="number of samples to average over (annealed)",
    )
    sigmaMask = Int(
        required=False,
        missing=30,
        help="spatial constant in um for computing residual variance of spike",
    )
    ThPre = Int(
        required=False,
        missing=8,
        help="threshold crossings for pre-clustering (in PCA projection space)",
    )

    spkTh = Int(
        required=False, missing=-6, help="spike threshold is standard deviations"
    )
    reorder = Int(
        required=False,
        missing=1,
        help="whether to reorder batches for drift correction",
    )
    nskip = Int(
        required=False,
        missing=25,
        help="how many batches to skip for determining spike PCs",
    )
    GPU = Int(
        required=False, missing=1, help="whether to run this code on an Nvidia GPU"
    )
    nfilt_factor = Int(
        required=False,
        missing=4,
        help="max number of clusters per good channel (even temporary ones)",
    )
    ntbuff = Int(
        required=False,
        missing=64,
        help="samples of symmetrical buffer for whitening and spike detection",
    )
    NT = String(
        required=False,
        missing="64*1024 + ops.ntbuff",
        help="this is the batch size; for GPU should be a multiple of 32 + ntbuff)",
    )
    whiteningRange = Int(required=False, missing=32)
    nSkipCov = Int(
        required=False, missing=25, help="compute whitening matrix from every Nth batch"
    )
    scaleproc = Int(required=False, missing=200, help="int16 scaling of whitenend data")
    nPCs = Int(
        required=False, missing=3, help="how many PCs to project the spikes into"
    )
    useRAM = Int(required=False, missing=0, help="must be 0")
    gain = Float(required=False, missing=1, help="uV/bit to report amplitudes in uV")
    CSBseed = Int(
        required=False, missing=1, help="random seed for clusterSingleBatches"
    )
    LTseed = Int(required=False, missing=1, help="random seed for learnTemplates")
    nNeighbors = Int(
        required=False, missing=32, help="number of channels to include in template"
    )
    CAR = Int(required=False, missing=1, help="1 to use CAR, 0 to skip")
    nblocks = Int(
        required=False,
        missing=5,
        help="for KS2.5 and KS3.0, set to 0 for rigid registration in drift correction, higher values non-rigid",
    )


class KilosortHelperParameters(Schema):

    kilosort_version = Int(
        required=False, missing=2, help="Kilosort version to use (1 or 2)"
    )

    spikeGLX_data = Bool(
        required=False,
        missing=False,
        help="If true, use SpikeGLX metafile to build chanMap",
    )
    ks_make_copy = Bool(
        required=False,
        missing=False,
        help="If true, make a copy of the original KS output",
    )

    surface_channel_buffer = Int(
        required=False,
        missing=15,
        help="Number of channels above brain surface to include in spike sorting",
    )
    noise_threshold = Float(
        required=False, missing=20.0, help="rms - median rms noise threhold, uV"
    )

    matlab_home_directory = InputDir(
        help="Location from which Matlab files can be copied and run."
    )
    kilosort_repository = InputDir(
        help="Local directory for the Kilosort source code repository."
    )
    npy_matlab_repository = InputDir(
        help="Local directory for the npy_matlab repo for writing phy output"
    )

    kilosort_params = Nested(
        KilosortParameters,
        required=False,
        help="Parameters used to auto-generate a Kilosort config file",
    )
    kilosort2_params = Nested(
        Kilosort2Parameters,
        required=False,
        help="Parameters used to auto-generate a Kilosort2 config file",
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    kilosort_helper_params = Nested(KilosortHelperParameters)

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

    execution_time = Float()
    kilosort_commit_hash = String()
    kilosort_commit_date = String()
    mask_channels = NumpyArray()
    nTemplate = Int()
    nTot = Int()


class KilosortHelperSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
