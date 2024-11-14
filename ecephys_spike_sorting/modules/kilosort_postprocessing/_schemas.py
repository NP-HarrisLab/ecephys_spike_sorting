from marshmallow import INCLUDE, Schema
from marshmallow.fields import Boolean, Float, Int, Nested, String

from ecephys_spike_sorting.modules.schema_fields import InputDir

from ...common.schemas import Directories, EphysParams


class PostprocessingParams(Schema):
    class Meta:
        unknown = INCLUDE

    within_unit_overlap_window = Float(
        required=False,
        missing=0.000166,
        help="Time window for removing overlapping spikes for one unit.",
    )
    between_unit_overlap_window = Float(
        required=False,
        missing=0.000166,
        help="Time window for removing overlapping spikes between two units.",
    )
    between_unit_dist_um = Int(
        required=False,
        missing=5,
        help="Number of channels (above and below peak channel) to search for overlapping spikes",
    )
    deletion_mode = String(
        required=False, missing="lowAmpCluster", help="lowAmpCluster or deleteFirst"
    )
    include_pcs = Boolean(
        required=False,
        missing=True,
        help="Set to false if features were not saved with Phy output",
    )
    remove_duplicates = Boolean(
        required=False, missing=True, help="Set to True for duplicate removal"
    )
    align_avg_waveform = Boolean(
        required=False,
        missing=True,
        help="Set to true to set spike times for mean waveform min = t0",
    )
    cWaves_path = InputDir(
        require=False, help="directory containing the CWaves executable."
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    ks_postprocessing_params = Nested(PostprocessingParams)
    directories = Nested(Directories)
    ephys_params = Nested(EphysParams)


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


class PostprocessingSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
