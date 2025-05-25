"""
Help Dialog Module

This module provides the Help dialog for the Nuitka GUI Compiler.
Displays usage instructions, feature highlights, and UI/UX improvements in a tabbed interface.

New in v1.4.0:
- Collapsible/expandable sections for option groups
- Modern themed look using ttk widgets
- Grouped rarely-used options in an "Advanced" section
- Modularized code for easier maintenance

License: GPL v3.0 (see LICENSE)
"""

import tkinter as tk
from tkinter import ttk, messagebox

class Help:
    """
    A class to display the Help dialog for the Nuitka application.
    
    This class provides a static method to show a modal dialog with
    help information organized in tabs for different topics.
    """
    
    @staticmethod
    def show_help(parent):
        """
        Display the Help dialog.
        
        This method creates and shows a modal dialog with help information
        organized in tabs. The dialog includes sections for usage instructions,
        features, and tips.
        
        Args:
            parent (tk.Tk): The parent window for the dialog
        """
        # Create and configure the help window
        help_window = tk.Toplevel(parent)
        help_window.title("Help")
        help_window.geometry("700x500")
        help_window.minsize(600, 400)
        
        # Center the window on screen
        window_width = 700
        window_height = 500
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        help_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- New Features Tab ---
        features_frame = ttk.Frame(notebook)
        notebook.add(features_frame, text="What's New")
        features_text = tk.Text(features_frame, wrap=tk.WORD, height=20)
        features_text.insert(tk.END, (
            "New in v1.4.0:\n"
            "- More advanced Nuitka options: MinGW64, UAC, metadata fields (company/product/version), UPX compression.\n"
            "- Improved error handling and input validation.\n"
            "- Advanced options grouped for easier navigation.\n"
            "- User feedback is clearer and more robust.\n"
        ))
        features_text.config(state=tk.DISABLED)
        features_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        # ===== USAGE TAB =====
        usage_frame = ttk.Frame(notebook, padding=10)
        notebook.add(usage_frame, text="Usage")
        usage_text = (
            "1. Select a Python file (*.py) using the 'Browse' button.\n"
            "2. (Optional) Choose the output directory for the compiled executable.\n"
            "3. (Optional) Select an icon file (ICO, EXE, or PNG) for your executable.\n"
            "4. (Optional) Configure Nuitka options: onefile, standalone, plugins, data files, jobs, LTO, Clang, and more.\n"
            "5. Click 'Compile' to start building your executable.\n"
            "6. View the output and logs in the lower section of the window."
        )
        usage_label = tk.Label(usage_frame, text=usage_text, justify=tk.LEFT, anchor='nw', wraplength=650)
        usage_label.pack(fill=tk.BOTH, expand=True)

        # ===== FEATURES TAB =====
        features_frame = ttk.Frame(notebook, padding=10)
        notebook.add(features_frame, text="Features")
        features_text = (
            "- Simple GUI for compiling Python scripts to executables with Nuitka\n"
            "- Support for Windows icon selection (ICO, EXE, PNG)\n"
            "- Automatic PNG to ICO conversion (requires Pillow)\n"
            "- Common Nuitka options: onefile, standalone, plugins, data files, jobs, LTO, Clang\n"
            "- Output directory selection\n"
            "- Log viewer and status messages\n"
            "- Error feedback and user-friendly dialogs\n"
            "- About, Help, and Sponsor dialogs\n"
            "- Designed for ease of use and quick setup\n"
            "\n"
            "Advanced Nuitka options now available:\n"
            "- Exclude/include modules and packages\n"
            "- Remove output directory before build\n"
            "- Show memory usage and progress\n"
            "- Enable PGO (Profile Guided Optimization)\n"
            "- Onefile compression selection\n"
            "- Python flags and more\n"
        )
        features_label = tk.Label(features_frame, text=features_text, justify=tk.LEFT, anchor='nw', wraplength=650)
        features_label.pack(fill=tk.BOTH, expand=True)

        # Close button
        close_btn = tk.Button(help_window, text="Close", command=help_window.destroy)
        close_btn.pack(pady=10)
        
        # Make the window modal
        help_window.transient(parent)
        help_window.grab_set()
        parent.wait_window(help_window)
