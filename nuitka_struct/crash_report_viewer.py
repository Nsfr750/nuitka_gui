"""
Crash Report Viewer for Nuitka GUI Compiler

This module provides a function to display the nuitka-crash-report.xml file in a scrollable dialog.
Useful for quickly viewing crash diagnostics from within the GUI.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

CRASH_REPORT_FILE = 'nuitka-crash-report.xml'

def show_crash_report(root):
    if not os.path.exists(CRASH_REPORT_FILE):
        messagebox.showerror("Crash Report Not Found", f"{CRASH_REPORT_FILE} not found.")
        return
    with open(CRASH_REPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    win = tk.Toplevel(root)
    win.title("Nuitka Crash Report")
    win.geometry("800x600")
    win.minsize(400, 300)
    text_area = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=('Consolas', 10))
    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # Browse button to open crash report in default editor
    def browse_crash_report():
        import subprocess
        import sys
        import os
        if os.path.exists(CRASH_REPORT_FILE):
            if sys.platform.startswith('win'):
                os.startfile(CRASH_REPORT_FILE)
            elif sys.platform.startswith('darwin'):
                subprocess.call(['open', CRASH_REPORT_FILE])
            else:
                subprocess.call(['xdg-open', CRASH_REPORT_FILE])
        else:
            tk.messagebox.showerror('Error', 'Crash report file not found.')

    browse_btn = tk.Button(win, text='Browse Crash Report', command=browse_crash_report)
    browse_btn.pack(pady=(0, 5))

    close_btn = tk.Button(win, text="Close", command=win.destroy)
    close_btn.pack(pady=10)
    win.transient(root)
    win.grab_set()
    root.wait_window(win)
