import tkinter as tk
from tkinter import ttk, scrolledtext
import os

# Define the name of the log file to be viewed
LOG_FILE = 'Nuitka.log'

class LogViewer:
    """
    A dialog to view the application log file.
    Provides a scrollable window to examine the contents of Nuitka.log.
    """
    @staticmethod
    def show_log(root):
        """
        Displays the log viewer dialog.
        
        :param root: The parent window of the log viewer dialog.
        """
        # Create a new top-level window for the log viewer
        log_window = tk.Toplevel(root)
        log_window.title('Application Log')
        log_window.geometry('700x500')
        log_window.minsize(500, 300)
        
        # Log text area
        text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=('Consolas', 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load log file content
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            text_area.insert(tk.END, content)
        else:
            text_area.insert(tk.END, 'Log file not found.')
        text_area.config(state=tk.DISABLED)
        
        # Browse button to open log file in default editor
        def browse_log():
            import subprocess
            import sys
            import os
            if os.path.exists(LOG_FILE):
                if sys.platform.startswith('win'):
                    os.startfile(LOG_FILE)
                elif sys.platform.startswith('darwin'):
                    subprocess.call(['open', LOG_FILE])
                else:
                    subprocess.call(['xdg-open', LOG_FILE])
            else:
                tk.messagebox.showerror('Error', 'Log file not found.')

        browse_btn = ttk.Button(log_window, text='Browse Log File', command=browse_log)
        browse_btn.pack(pady=(0, 5))

        # Close button
        close_btn = ttk.Button(log_window, text='Close', command=log_window.destroy)
        close_btn.pack(pady=10)
        
        log_window.transient(root)
        log_window.grab_set()
        root.wait_window(log_window)
