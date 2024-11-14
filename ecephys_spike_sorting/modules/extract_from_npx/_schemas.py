from marshmallow import INCLUDE, Schema
from marshmallow.fields import Dict, Float, InputDir, Int, Nested, String

from ...common.schemas import CommonFiles, Directories, EphysParams


class ExtractFromNpxParams(Schema):
    class Meta:
        unknown = INCLUDE

    npx_directory = String(help="Path to NPX file(s) saved by Open Ephys")
    settings_xml = String(help="Path to settings.xml file saved by Open Ephys")
    npx_extractor_executable = String(
        help="Path to .exe file for NPX extraction (Windows only)"
    )
    npx_extractor_repo = String(
        required=False,
        missing="None",
        help="Path to local repository for NPX extractor",
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    extract_from_npx_params = Nested(ExtractFromNpxParams)
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

    npx_extractor_execution_time = Float()
    settings_json = String()
    npx_extractor_commit_hash = String()
    npx_extractor_commit_date = String()


class NpxSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
