import os

import numpy as np
from marshmallow import Schema, ValidationError, fields


class NumpyArray(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        # Convert numpy array to list for serialization
        if isinstance(value, np.ndarray):
            return value.tolist()
        else:
            raise ValidationError("Expected a numpy array for serialization")

    def _deserialize(self, value, attr, data, **kwargs):
        # Convert list back to numpy array for deserialization
        try:
            return np.array(value)
        except ValueError as e:
            raise ValidationError("Invalid data for numpy array") from e


class InputDir(fields.Field):
    """Custom field to validate that an input path is an existing directory."""

    def _deserialize(self, value, attr, data, **kwargs):
        # Check if the path exists and is a directory
        if not os.path.isdir(value):
            raise ValidationError(f"The path '{value}' is not a valid directory.")
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        return value


class OutputDir(fields.Field):
    """Custom field to validate that an input path is a valid directory,
    and create the directory if it doesn't exist."""

    def _deserialize(self, value, attr, data, **kwargs):
        # Check if the path exists, and if not, create it
        if not os.path.exists(value):
            try:
                os.makedirs(value)
            except OSError as e:
                raise ValidationError(f"Could not create directory '{value}': {e}")
        elif not os.path.isdir(value):
            raise ValidationError(
                f"The path '{value}' exists, but it is not a directory."
            )
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        return value


class OutputFile(fields.Field):
    """Custom field to validate that an input path is a valid file,
    and create the file if it doesn't exist."""

    def _deserialize(self, value, attr, data, **kwargs):
        # Check if the file exists
        if not os.path.exists(value):
            try:
                # If the file doesn't exist, create an empty file
                with open(value, "w"):
                    pass
            except OSError as e:
                raise ValidationError(f"Could not create file '{value}': {e}")
        elif not os.path.isfile(value):
            raise ValidationError(f"The path '{value}' exists, but it is not a file.")
        return value

    def _serialize(self, value, attr, obj, **kwargs):
        return value