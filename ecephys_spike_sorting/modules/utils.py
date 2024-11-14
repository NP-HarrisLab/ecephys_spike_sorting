import json

import numpy as np


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert numpy array to list
        elif isinstance(obj, (np.integer, np.floating)):  # Handle numpy scalar types
            return obj.item()
        elif isinstance(obj, np.bool_):  # Handle numpy booleans
            return bool(obj)
        return super().default(obj)
