"""
Menu Bar Module for Nuitka GUI Compiler

Defines the menu bar and menu actions for the Nuitka GUI Compiler.
Handles File, Log, and Info menus, and attaches them to the main window.
"""

import tkinter as tk
from nuitka_struct.about import About
from nuitka_struct.help import Help
from nuitka_struct.sponsor import Sponsor
from nuitka_struct import version
from nuitka_struct.log_viewer import LogViewer
from nuitka_struct import crash_report_viewer


def create_menu_bar(root, app):
    """
    Create the application menu bar and attach it to the root window.
    Args:
        root: The main Tkinter root window
        app: The main app instance (for callbacks)
    """
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Optionally, add File menu for Exit
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # Log menu (placeholder, implement log view if needed)
    log_menu = tk.Menu(menubar, tearoff=0)
    log_menu.add_command(label="View Log", command=lambda: LogViewer.show_log(root))
    log_menu.add_command(label="View Crash Report", command=lambda: crash_report_viewer.show_crash_report(root))
    menubar.add_cascade(label="Log", menu=log_menu)
    
    # Info menu
    info_menu = tk.Menu(menubar, tearoff=0)
    info_menu.add_command(label="About", command=lambda: About.show_about(root))
    info_menu.add_command(label="Help", command=lambda: Help.show_help(root))
    info_menu.add_command(label="Sponsor", command=lambda: Sponsor.show_sponsor(root))
    menubar.add_cascade(label="Info", menu=info_menu)

    return menubar
