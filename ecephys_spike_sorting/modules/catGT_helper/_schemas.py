from argschema import ArgSchema, ArgSchemaParser
from argschema.fields import Bool, Dict, Float, InputDir, Int, Nested, String
from argschema.schemas import DefaultSchema

from ...common.schemas import Directories, EphysParams


class CatGTParams(DefaultSchema):
    run_name = String(required=True, help="undecorated run name (no g or t indices")
    gate_string = String(required=True, default="0", help="gate string")
    trigger_string = String(
        required=True,
        default="0,0",
        help="string specifying trials to concatenate, e.g. 0,200",
    )
    probe_string = String(
        required=True, default="0", help="string specifying probes, e.g. 0:3"
    )
    stream_string = String(
        required=True, default="-ap", help="string specifying which streams to process"
    )
    car_mode = String(
        require=False,
        default="None",
        help="Comaon average reference mode. Must = None, gbldmx, or loccar ",
    )
    loccar_inner = Int(
        require=False, default=2, help="Inner radius for loccar in sites"
    )
    loccar_outer = Int(
        require=False, default=8, help="Outer radius for loccar in sites"
    )
    loccar_inner_um = Int(
        require=False, default=40, help="Inner radius for loccar in um"
    )
    loccar_outer_um = Int(
        require=False, default=40, help="Outer radius for loccar in um"
    )
    maxZ_um = Float(
        require=False,
        default=-1,
        help="If > -1, maximum z from bottom row to analyze and save",
    )
    useGeom = Bool(
        require=False, default=True, help="use snsGeomMap for loccar and depth"
    )
    cmdStr = String(
        required=True,
        default="-prbfld -aphipass=300 -gbldmx -gfix=0.40,0.10,0.02",
        help="input stream filter, error correct and extract settings for CatGT",
    )
    catGTPath = InputDir(help="directory containing the CatGT executable.")


class InputParameters(ArgSchema):

    catGT_helper_params = Nested(CatGTParams)
    directories = Nested(Directories)
    ephys_params = Nested(EphysParams)


class OutputSchema(DefaultSchema):
    input_parameters = Nested(
        InputParameters,
        description=("Input parameters the module " "was run with"),
        required=True,
    )


class OutputParameters(OutputSchema):

    execution_time = Float()
