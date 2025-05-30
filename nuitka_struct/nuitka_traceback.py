"""
Traceback Logger for Nuitka GUI Compiler

This module provides a function to log uncaught exceptions and tracebacks to Nuitka.log.
Allows errors to be viewed from the GUI Log Viewer. Integrates with sys.excepthook.
"""

import sys
import traceback as _std_traceback
import datetime

LOG_FILE = 'Nuitka.log'

def log_exception(exc_type, exc_value, exc_tb):
    """
    Logs uncaught exceptions and their tracebacks to Nuitka.log.
    """
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Uncaught exception:\n")
        _std_traceback.print_exception(exc_type, exc_value, exc_tb, file=f)

def get_traceback_module():
    """
    Returns the standard library traceback module (for use in main.py if needed).
    """
    return _std_traceback

# To enable global exception logging, add this to main.py:
# import traceback as tb_logger
# sys.excepthook = tb_logger.log_exception
# traceback = tb_logger.get_traceback_module()  # if you need the standard library traceback
