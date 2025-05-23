import os

from marshmallow import Schema
from marshmallow.fields import Boolean, Field, Float, Integer, List, String


class InputFile(Field):
    default_error_messages = {
        "invalid": "Not a valid filepath",
        "not_found": "File not found",
        "not_file": "Not a file",
    }

    def __init__(self, *args, check_exists=False, **kwargs):
        self.check_exists = check_exists
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        # Ensure value is a string
        if not isinstance(value, str):
            self.fail("invalid")
        # Normalize the path
        value = os.path.abspath(value)
        value = os.path.normpath(value)
        # Ensure the file exists
        if self.check_exists and self.required and value is not None:
            print(value)
            if not os.path.exists(value):
                self.fail("not_found")
            # Ensure the path is a file
            if not os.path.isfile(value):
                self.fail("not_file")
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        return os.path.normpath(value) if value else None


class InputDir(Field):
    default_error_messages = {
        "invalid": "Not a valid filepath",
        "not_found": "Directory not found",
        "not_dir": "Not a directory",
    }

    def __init__(self, *args, check_exists=False, create=False, **kwargs):
        self.check_exists = check_exists
        self.create = create
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        # Ensure value is a string
        if not isinstance(value, str):
            self.fail("invalid")

        # Ensure the file exists
        if self.create:
            os.makedirs(value, exist_ok=True)

        if self.check_exists:
            if not os.path.exists(value):
                self.fail("not_found")
            # Ensure the path is a directory
            if not os.path.isdir(value):
                self.fail("not_dir")
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        return os.path.normpath(value) if value else None


class CreateInputJsonParams(Schema):
    ecephys_directory = InputDir(
        required=True,
        check_exists=True,
        description="Path to the ecephys directory. The one within the repository.",
    )
    kilosort_25_repository = InputDir(
        required=False,
        check_exists=True,
        description="Path to the kilosort 2.5 repository",
    )
    npy_matlab_repository = InputDir(
        required=True,
        check_exists=True,
        description="Path to the npy-matlab repository",
    )
    catGTPath = InputDir(
        required=True,
        check_exists=True,
        description="Path to the catGT repository",
    )
    tPrime_path = InputDir(
        required=True,
        check_exists=True,
        description="Path to the tPrime repository",
    )
    cWaves_path = InputDir(
        required=True,
        check_exists=True,
        description="Path to the cWaves repository",
    )


class SglxMultiRunPipelineParams(Schema):
    ks_ver = String(required=True, description="Kilosort version")
    npx_directory = InputDir(
        required=True, check_exists=True, description="Path to the npx directory"
    )
    run_name = String(required=True, description="Name of the run")
    gate_index = String(required=False, description="Gate index", missing="0")
    triggers = String(required=False, description="Triggers", missing="0,0")
    probes = String(
        required=False, description="Probes. Default : will process all", missing=":"
    )
    run_CatGT = Boolean(required=False, description="Run CatGT", missing=True)
    process_lf = Boolean(required=False, description="Process Lf", missing=False)
    ni_present = Boolean(required=False, description="NI Present", missing=False)
    ni_extract_string = String(
        required=False,
        description="NI Extract String",
        missing="-xa=0,0,0,1,3,500 -xia=0,0,1,3,3,0 -xd=0,0,-1,1,50 -xid=0,0,-1,2,1.7 -xid=0,0,-1,3,5",
    )
    runTPrime = Boolean(required=False, description="Run TPrime", missing=True)
    run_kilosort = Boolean(
        required=False, description="Run Kilosort module", missing=True
    )
    run_kilosort_postprocessing = Boolean(
        required=False, description="Run Kilosort Postprocessing module", missing=True
    )
    run_noise_templates = Boolean(
        required=False, description="Run Noise Templates module", missing=False
    )
    run_mean_waveforms = Boolean(
        required=False, description="Run Mean Waveforms module", missing=True
    )
    run_quality_metrics = Boolean(
        required=False, description="Run Quality Metrics module", missing=True
    )
    startsecs = Float(
        required=False,
        description="Start time for input stream in seconds",
        missing=None,
    )
    maxsecs = Float(
        required=False,
        description="Maximum time for input stream in seconds",
        missing=None,
    )
    supercat = Boolean(
        required=False,
        description="Run supercat module",
        missing=False,
    )
    supercat_folders = List(
        String,
        required=False,
        description="List of folders to supercat",
        missing=[],
    )
    run_supercat = Boolean(
        required=False,
        description="Run supercat",
        missing=False,
    )
    trim_edges = Boolean(
        required=False,
        description="Trim edges",
        missing=False,
    )
