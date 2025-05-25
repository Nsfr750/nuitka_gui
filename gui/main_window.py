import tkinter as tk
from menu import create_menu_bar
from gui.options_panel import OptionsPanel

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nuitka GUI Compiler")
        # Menu bar
        create_menu_bar(self, self)
        # Variables
        self.file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_filename = tk.StringVar()
        # Layout main input widgets (stub, for now)
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        self.labels['python_file'] = tk.Label(self, text="Python file:")
        self.labels['python_file'].grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entries['file_path'] = tk.Entry(self, textvariable=self.file_path, width=40)
        self.entries['file_path'].grid(row=0, column=1, padx=5, pady=5)
        self.buttons['browse_file'] = tk.Button(self, text="Browse", command=self.browse_file)
        self.buttons['browse_file'].grid(row=0, column=2, padx=5, pady=5)
        self.labels['output_dir'] = tk.Label(self, text="Output directory:")
        self.labels['output_dir'].grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entries['output_dir'] = tk.Entry(self, textvariable=self.output_dir, width=40)
        self.entries['output_dir'].grid(row=1, column=1, padx=5, pady=5)
        self.buttons['browse_output_dir'] = tk.Button(self, text="Browse", command=self.browse_output_dir)
        self.buttons['browse_output_dir'].grid(row=1, column=2, padx=5, pady=5)
        self.labels['output_filename'] = tk.Label(self, text="Output filename:")
        self.labels['output_filename'].grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entries['output_filename'] = tk.Entry(self, textvariable=self.output_filename, width=40)
        self.entries['output_filename'].grid(row=2, column=1, padx=5, pady=5)
        # Advanced options panel
        self.options_panel = OptionsPanel(self)
        self.options_panel.grid(row=3, column=0, columnspan=3, sticky="we", padx=5, pady=10)
        # Compile button
        self.buttons['compile'] = tk.Button(self, text="Compile", command=self.compile_file)
        self.buttons['compile'].grid(row=4, column=0, columnspan=2, pady=10)
        # Log box
        self.log_box = tk.Text(self, height=12, state='disabled', wrap='word')
        self.log_box.grid(row=5, column=0, columnspan=3, sticky="we", padx=5, pady=5)
    def browse_file(self):
        pass
    def browse_output_dir(self):
        pass
    def compile_file(self):
        from compiler.command_builder import build_nuitka_command
        from compiler.runner import run_nuitka_command
        # Gather main fields
        main_state = {
            'file_path': self.file_path.get().strip(),
            'output_dir': self.output_dir.get().strip(),
            'output_filename': self.output_filename.get().strip(),
            # Add other main fields as needed
        }
        # Gather advanced options from OptionsPanel
        options_panel = self.options_panel
        options_state = {k: v.get() if hasattr(v, 'get') else v for k, v in vars(options_panel).items() if isinstance(v, (tk.StringVar, tk.BooleanVar, tk.IntVar))}
        # Build command
        cmd = build_nuitka_command(main_state, options_state)
        self.append_log(f"Running: {' '.join(cmd)}\n")
        # Run Nuitka (stub handlers for now)
        run_nuitka_command(cmd, self._show_success, self._show_error)
    def append_log(self, text):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, text)
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')
    def _show_success(self, msg):
        self.append_log(f"SUCCESS: {msg}\n")
    def _show_error(self, msg):
        self.append_log(f"ERROR: {msg}\n")
