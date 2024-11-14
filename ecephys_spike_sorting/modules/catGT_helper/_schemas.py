from marshmallow import INCLUDE, Schema
from marshmallow.fields import Bool, Float, Int, Nested, String

from ecephys_spike_sorting.modules.schema_fields import InputDir

from ...common.schemas import Directories, EphysParams


class CatGTParams(Schema):
    class Meta:
        unknown = INCLUDE

    run_name = String(required=True, help="undecorated run name (no g or t indices")
    gate_string = String(required=True, help="gate string")
    trigger_string = String(
        required=True,
        help="string specifying trials to concatenate, e.g. 0,200",
    )
    probe_string = String(required=True, help="string specifying probes, e.g. 0:3")
    stream_string = String(
        required=True, help="string specifying which streams to process"
    )
    car_mode = String(
        require=False,
        missing="None",
        help="Common average reference mode. Must = None, gbldmx, or loccar ",
    )
    loccar_inner = Int(
        require=False, missing=2, help="Inner radius for loccar in sites"
    )
    loccar_outer = Int(
        require=False, missing=8, help="Outer radius for loccar in sites"
    )
    loccar_inner_um = Int(
        require=False, missing=40, help="Inner radius for loccar in um"
    )
    loccar_outer_um = Int(
        require=False, missing=40, help="Outer radius for loccar in um"
    )
    maxZ_um = Float(
        require=False,
        missing=-1,
        help="If > -1, maximum z from bottom row to analyze and save",
    )
    useGeom = Bool(
        require=False, missing=True, help="use snsGeomMap for loccar and depth"
    )
    cmdStr = String(
        required=True,
        help="input stream filter, error correct and extract settings for CatGT",
    )
    catGTPath = InputDir(help="directory containing the CatGT executable.")


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

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


class CatgtSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
