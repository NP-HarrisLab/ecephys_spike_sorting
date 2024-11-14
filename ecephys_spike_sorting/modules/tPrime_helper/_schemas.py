from marshmallow import INCLUDE, Schema
from marshmallow.fields import Boolean, Float, List, Nested, String

from ecephys_spike_sorting.modules.schema_fields import InputDir

from ...common.schemas import Directories, EphysParams
from ..catGT_helper._schemas import CatGTParams


class tPrimeParams(Schema):
    class Meta:
        unknown = INCLUDE

    tPrime_path = InputDir(help="directory containing the TPrime executable.")
    sync_period = Float(missing=1.0, help="Period of sync waveform (sec).")
    toStream_sync_params = String(
        required=False,
        missing="imec0",
        help="stream identifier for tostream, imec<index>, ni, or obx<index>",
    )
    ni_sync_params = String(
        required=False, missing="", help="deprecated, now read from fyi file"
    )
    ni_ex_list = String(
        required=False, missing="", help="deprecated, now read from fyi file"
    )
    im_ex_list = String(
        required=False, missing="", help="deprecated, now read from fyi file"
    )
    tPrime_3A = Boolean(required=False, missing=False, help="is this 3A data?")
    toStream_path_3A = String(required=False, help="full path to toStream edges file")
    fromStream_list_3A = List(
        String, required=False, help="list of full paths to fromStream edges files"
    )
    psth_ex_str = String(
        required=False, help="extract string for events.csv for phy psth"
    )
    sort_out_tag = String(required=False, help="tag for sort output (phy) folder")


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    tPrime_helper_params = Nested(tPrimeParams)
    catGT_helper_params = Nested(CatGTParams)
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


class TprimeSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
