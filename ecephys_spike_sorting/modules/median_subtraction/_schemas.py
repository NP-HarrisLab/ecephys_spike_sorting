from marshmallow import INCLUDE, Schema
from marshmallow.fields import Float, Nested, String

from ...common.schemas import CommonFiles, Directories, EphysParams


class MedianSubtractionParams(Schema):
    class Meta:
        unknown = INCLUDE

    median_subtraction_executable = String(
        help="Path to .exe used for median subtraction (Windows only)"
    )
    median_subtraction_repo = String(
        help="Path to local repository for median subtraction executable"
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    median_subtraction_params = Nested(MedianSubtractionParams)
    common_files = Nested(CommonFiles)
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

    median_subtraction_execution_time = Float()
    median_subtraction_commit_hash = String()
    median_subtraction_commit_date = String()


class MedianSubtractionSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
