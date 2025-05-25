# Input validation helpers for Nuitka GUI

import os

def validate_python_file(path):
    return os.path.isfile(path) and path.endswith('.py')

def validate_output_dir(path):
    return os.path.isdir(path)
