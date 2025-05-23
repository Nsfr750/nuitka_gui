import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import traceback as tb_logger
sys.excepthook = tb_logger.log_exception
traceback = tb_logger.get_traceback_module()
from menu import create_menu_bar

class NuitkaGUI:
    """
    Main GUI class for the Nuitka GUI Compiler.
    Handles all widget creation, layout, and user interactions.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Nuitka GUI Compiler")
        self.file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_filename = tk.StringVar()  # New: store custom output filename
        self.onefile = tk.BooleanVar(value=True)
        self.standalone = tk.BooleanVar(value=False)
        self.custom_opts = tk.StringVar()
        self.plugins = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.icon_type = tk.StringVar(value="ico")  # "ico", "exe", or "png"
        self.png_to_ico_path = None  # Store path to generated .ico file from .png
        self.disable_console = tk.BooleanVar(value=False)
        self.data_files = tk.StringVar()
        self.follow_imports = tk.BooleanVar(value=False)
        self.lto = tk.BooleanVar(value=False)
        self.clang = tk.BooleanVar(value=False)
        self.jobs = tk.IntVar(value=1)

        # Menu bar
        create_menu_bar(self.root, self)

        # --- UI Elements ---
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        self.checkbuttons = {}
        self.radiobuttons = {}

        # Layout (store references for updates)
        self.labels['python_file'] = tk.Label(root, text="Python file:")
        self.labels['python_file'].grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entries['file_path'] = tk.Entry(root, textvariable=self.file_path, width=40)
        self.entries['file_path'].grid(row=0, column=1, padx=5, pady=5)
        self.buttons['browse_file'] = tk.Button(root, text="Browse", command=self.browse_file)
        self.buttons['browse_file'].grid(row=0, column=2, padx=5, pady=5)

        self.labels['output_dir'] = tk.Label(root, text="Output directory:")
        self.labels['output_dir'].grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entries['output_dir'] = tk.Entry(root, textvariable=self.output_dir, width=40)
        self.entries['output_dir'].grid(row=1, column=1, padx=5, pady=5)
        self.buttons['browse_output_dir'] = tk.Button(root, text="Browse", command=self.browse_output_dir)
        self.buttons['browse_output_dir'].grid(row=1, column=2, padx=5, pady=5)

        # Output filename
        self.labels['output_filename'] = tk.Label(root, text="Output filename:")
        self.labels['output_filename'].grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entries['output_filename'] = tk.Entry(root, textvariable=self.output_filename, width=40)
        self.entries['output_filename'].grid(row=2, column=1, padx=5, pady=5)

        # Splash screen image
        self.splash_image_path = tk.StringVar()
        self.splash_timeout = tk.IntVar(value=3)
        self.labels['splash_image'] = tk.Label(root, text="Splash image (Windows, .png):")
        self.labels['splash_image'].grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.entries['splash_image'] = tk.Entry(root, textvariable=self.splash_image_path, width=20)
        self.entries['splash_image'].grid(row=2, column=3, padx=5, pady=5)
        self.buttons['browse_splash'] = tk.Button(root, text="Browse", command=self.browse_splash_image)
        self.buttons['browse_splash'].grid(row=2, column=4, padx=5, pady=5)
        self.labels['splash_timeout'] = tk.Label(root, text="Splash timeout (s):")
        self.labels['splash_timeout'].grid(row=3, column=2, sticky="e", padx=5, pady=5)
        self.entries['splash_timeout'] = tk.Spinbox(root, from_=1, to=30, textvariable=self.splash_timeout, width=5)
        self.entries['splash_timeout'].grid(row=3, column=3, padx=5, pady=5)

        self.checkbuttons['onefile'] = tk.Checkbutton(root, text="--onefile", variable=self.onefile)
        self.checkbuttons['onefile'].grid(row=3, column=0, sticky="w", padx=5)
        self.checkbuttons['standalone'] = tk.Checkbutton(root, text="--standalone", variable=self.standalone)
        self.checkbuttons['standalone'].grid(row=3, column=1, sticky="w", padx=5)
        self.checkbuttons['disable_console'] = tk.Checkbutton(root, text="--windows-disable-console", variable=self.disable_console)
        self.checkbuttons['disable_console'].grid(row=3, column=2, sticky="w", padx=5)

        self.labels['plugins'] = tk.Label(root, text="--enable-plugin(s):")
        self.labels['plugins'].grid(row=3, column=0, sticky="e", padx=5)
        self.entries['plugins'] = tk.Entry(root, textvariable=self.plugins, width=25)
        self.entries['plugins'].grid(row=3, column=1, sticky="w", padx=5)
        self.labels['plugins_hint'] = tk.Label(root, text="comma-separated")
        self.labels['plugins_hint'].grid(row=3, column=2, sticky="w")

        self.labels['icon'] = tk.Label(root, text="Windows icon:")
        self.labels['icon'].grid(row=4, column=0, sticky="e", padx=5)
        # Frame to group icon entry and browse button
        icon_frame = tk.Frame(root)
        icon_frame.grid(row=4, column=1, sticky="w", padx=5)
        self.entries['icon_path'] = tk.Entry(icon_frame, textvariable=self.icon_path, width=25)
        self.entries['icon_path'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.buttons['browse_icon'] = tk.Button(icon_frame, text="Browse", command=self.browse_icon_file)
        self.buttons['browse_icon'].pack(side=tk.LEFT, padx=3)
        # Tooltip for icon browse
        def show_icon_tip(event):
            messagebox.showinfo("Icon Selection", "Browse for an ICO, EXE, or PNG file depending on the selected icon type.")
        self.buttons['browse_icon'].bind('<Button-3>', show_icon_tip)
        self.radiobuttons['ico'] = tk.Radiobutton(root, text="ICO", variable=self.icon_type, value="ico")
        self.radiobuttons['ico'].grid(row=4, column=2, sticky="w", padx=5)
        self.radiobuttons['exe'] = tk.Radiobutton(root, text="EXE", variable=self.icon_type, value="exe")
        self.radiobuttons['exe'].grid(row=4, column=2, sticky="e", padx=55)
        self.radiobuttons['png'] = tk.Radiobutton(root, text="PNG", variable=self.icon_type, value="png")
        self.radiobuttons['png'].grid(row=4, column=2, sticky="e", padx=5)

        self.labels['data_files'] = tk.Label(root, text="--include-data-files:")
        self.labels['data_files'].grid(row=5, column=0, sticky="e", padx=5)
        self.entries['data_files'] = tk.Entry(root, textvariable=self.data_files, width=25)
        self.entries['data_files'].grid(row=5, column=1, sticky="w", padx=5)
        self.labels['data_files_hint'] = tk.Label(root, text="pattern=dest, ...")
        self.labels['data_files_hint'].grid(row=5, column=2, sticky="w")

        self.checkbuttons['follow_imports'] = tk.Checkbutton(root, text="--follow-imports", variable=self.follow_imports)
        self.checkbuttons['follow_imports'].grid(row=6, column=0, sticky="w", padx=5)
        self.checkbuttons['lto'] = tk.Checkbutton(root, text="--lto", variable=self.lto)
        self.checkbuttons['lto'].grid(row=6, column=1, sticky="w", padx=5)
        self.checkbuttons['clang'] = tk.Checkbutton(root, text="--clang", variable=self.clang)
        self.checkbuttons['clang'].grid(row=6, column=2, sticky="w", padx=5)

        self.labels['jobs'] = tk.Label(root, text="--jobs:")
        self.labels['jobs'].grid(row=7, column=0, sticky="e", padx=5)
        self.entries['jobs'] = tk.Spinbox(root, from_=1, to=16, textvariable=self.jobs, width=5)
        self.entries['jobs'].grid(row=7, column=1, sticky="w", padx=5)

        # Advanced Nuitka options
        self.labels['exclude_modules'] = tk.Label(root, text="Exclude modules/packages:")
        self.labels['exclude_modules'].grid(row=8, column=0, sticky="e", padx=5)
        self.exclude_modules = tk.StringVar()
        self.entries['exclude_modules'] = tk.Entry(root, textvariable=self.exclude_modules, width=25)
        self.entries['exclude_modules'].grid(row=8, column=1, sticky="w", padx=5)
        self.labels['exclude_hint'] = tk.Label(root, text="comma-separated")
        self.labels['exclude_hint'].grid(row=8, column=2, sticky="w")

        self.labels['include_modules'] = tk.Label(root, text="Include modules:")
        self.labels['include_modules'].grid(row=9, column=0, sticky="e", padx=5)
        self.include_modules = tk.StringVar()
        self.entries['include_modules'] = tk.Entry(root, textvariable=self.include_modules, width=25)
        self.entries['include_modules'].grid(row=9, column=1, sticky="w", padx=5)
        self.labels['include_hint'] = tk.Label(root, text="comma-separated")
        self.labels['include_hint'].grid(row=9, column=2, sticky="w")

        self.checkbuttons['remove_output'] = tk.Checkbutton(root, text="--remove-output", variable=tk.BooleanVar(value=False))
        self.checkbuttons['remove_output'].grid(row=10, column=0, sticky="w", padx=5)
        self.checkbuttons['show_memory'] = tk.Checkbutton(root, text="--show-memory", variable=tk.BooleanVar(value=False))
        self.checkbuttons['show_memory'].grid(row=10, column=1, sticky="w", padx=5)
        self.checkbuttons['show_progress'] = tk.Checkbutton(root, text="--show-progress", variable=tk.BooleanVar(value=False))
        self.checkbuttons['show_progress'].grid(row=10, column=2, sticky="w", padx=5)
        self.checkbuttons['pgo'] = tk.Checkbutton(root, text="--pgo", variable=tk.BooleanVar(value=False))
        self.checkbuttons['pgo'].grid(row=11, column=0, sticky="w", padx=5)
        self.checkbuttons['no_dependency_cache'] = tk.Checkbutton(root, text="--no-dependency-cache", variable=tk.BooleanVar(value=False))
        self.checkbuttons['no_dependency_cache'].grid(row=11, column=1, sticky="w", padx=5)

        self.labels['onefile_compression'] = tk.Label(root, text="Onefile compression:")
        self.labels['onefile_compression'].grid(row=12, column=0, sticky="e", padx=5)
        self.onefile_compression = tk.StringVar(value="auto")
        self.entries['onefile_compression'] = tk.OptionMenu(root, self.onefile_compression, "auto", "lzma", "none")
        self.entries['onefile_compression'].grid(row=12, column=1, sticky="w", padx=5)

        self.labels['python_flags'] = tk.Label(root, text="Python flags:")
        self.labels['python_flags'].grid(row=13, column=0, sticky="e", padx=5)
        self.python_flags = tk.StringVar()
        self.entries['python_flags'] = tk.Entry(root, textvariable=self.python_flags, width=25)
        self.entries['python_flags'].grid(row=13, column=1, sticky="w", padx=5)
        self.labels['python_flags_hint'] = tk.Label(root, text="comma-separated")
        self.labels['python_flags_hint'].grid(row=13, column=2, sticky="w")

        self.labels['custom_opts'] = tk.Label(root, text="Custom Nuitka options:")
        self.labels['custom_opts'].grid(row=14, column=0, sticky="e", padx=5)
        self.entries['custom_opts'] = tk.Entry(root, textvariable=self.custom_opts, width=40)
        self.entries['custom_opts'].grid(row=14, column=1, columnspan=2, padx=5, pady=5, sticky="we")

        from tkinter import ttk
        # Progress bar for compilation (left of Compile button)
        self.progress = ttk.Progressbar(root, mode='indeterminate', length=120)
        self.progress.grid(row=15, column=0, sticky="e", padx=(10, 5), pady=10)
        self.buttons['compile'] = tk.Button(root, text="Compile", command=self.compile_file)
        self.buttons['compile'].grid(row=15, column=1, sticky="w", padx=(5, 2), pady=10)
        self.buttons['stop_compile'] = tk.Button(root, text="Stop Compiling", command=self.stop_compiling, state='disabled')
        self.buttons['stop_compile'].grid(row=15, column=2, sticky="w", padx=(2, 10), pady=10)
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.grid(row=16, column=0, columnspan=3)
        self.progress.grid_remove()  # Hide initially

        self.labels['output'] = tk.Label(root, text="Output:")
        self.labels['output'].grid(row=11, column=0, sticky="ne", padx=5)
        self.log_box = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')
        self.log_box.grid(row=11, column=1, columnspan=2, padx=5, pady=5, sticky="we")

        root.grid_columnconfigure(1, weight=1)
        root.resizable(True, True)

    def browse_icon_file(self):
        icon_type = self.icon_type.get()
        if icon_type == "ico":
            filetypes = [("Icon Files", "*.ico")]
        elif icon_type == "exe":
            filetypes = [("Executable Files", "*.exe")]
        else:
            filetypes = [("PNG Files", "*.png")]
        file = filedialog.askopenfilename(filetypes=filetypes)
        if file:
            self.icon_path.set(file)

    def browse_splash_image(self):
        file = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if file:
            self.splash_image_path.set(file)

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file:
            self.file_path.set(file)

    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def compile_file(self):
        file = self.file_path.get()
        outdir = self.output_dir.get()
        if not file or not os.path.isfile(file):
            messagebox.showerror("Error", "Please select a valid Python file.")
            return
        if outdir and not os.path.isdir(outdir):
            messagebox.showerror("Error", "Please select a valid output directory.")
            return
        splash_img = self.splash_image_path.get().strip()
        splash_timeout = self.splash_timeout.get()
        if splash_img:
            # Show splash image for splash_timeout seconds before compiling
            try:
                from PIL import Image, ImageTk
                splash_win = tk.Toplevel(self.root)
                splash_win.overrideredirect(True)
                img = Image.open(splash_img)
                tk_img = ImageTk.PhotoImage(img)
                label = tk.Label(splash_win, image=tk_img)
                label.pack()
                splash_win.update_idletasks()
                # Center splash
                w, h = img.size
                x = (self.root.winfo_screenwidth() // 2) - (w // 2)
                y = (self.root.winfo_screenheight() // 2) - (h // 2)
                splash_win.geometry(f"{w}x{h}+{x}+{y}")
                self.root.after(splash_timeout * 1000, splash_win.destroy)
                self.root.update()
                splash_win.after(splash_timeout * 1000, splash_win.destroy)
                splash_win.mainloop()
            except Exception as e:
                self.append_log(f"Splash error: {e}\n")
        self.status_label.config(text="Compiling...", fg="blue")
        self.buttons['compile'].config(state='disabled')
        self.buttons['stop_compile'].config(state='normal')
        self.progress.grid()  # Show progress bar
        self.progress.start(10)
        self.log_box.config(state='normal')
        self.log_box.delete(1.0, tk.END)
        self.log_box.config(state='disabled')
        self._compiling = True
        threading.Thread(target=self.run_nuitka, args=(file, outdir), daemon=True).start()

    def run_nuitka(self, file, outdir):
        self._nuitka_proc = None
        try:
            cmd = [sys.executable, "-m", "nuitka"]
            # Basic options
            if self.onefile.get():
                cmd.append("--onefile")
            if self.standalone.get():
                cmd.append("--standalone")
            if outdir:
                cmd.extend([f"--output-dir={outdir}"])
            # New options
            if self.disable_console.get():
                cmd.append("--windows-disable-console")
            plugins = self.plugins.get().strip()
            if plugins:
                for plugin in plugins.split(","):
                    plugin = plugin.strip()
                    if plugin:
                        cmd.append(f"--enable-plugin={plugin}")
            icon = self.icon_path.get().strip()
            icon_type = self.icon_type.get()
            if icon:
                if icon_type == "ico":
                    cmd.append(f"--windows-icon-from-ico={icon}")
                elif icon_type == "exe":
                    cmd.append(f"--windows-icon-from-exe={icon}")
                elif icon_type == "png":
                    # Convert PNG to ICO
                    try:
                        from PIL import Image
                        import tempfile
                        img = Image.open(icon)
                        tmp_ico = tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
                        img.save(tmp_ico.name, format="ICO")
                        self.png_to_ico_path = tmp_ico.name
                        cmd.append(f"--windows-icon-from-ico={self.png_to_ico_path}")
                    except ImportError:
                        self.append_log("Pillow is required for PNG to ICO conversion. Please install with 'pip install pillow'.\n")
                        self.status_label.config(text="Missing Pillow library", fg="red")
                        self.buttons['compile'].config(state='normal')
                        self.buttons['stop_compile'].config(state='disabled')
                        self._compiling = False
                        return
                    except Exception as e:
                        self.append_log(f"Error converting PNG to ICO: {e}\n")
                        self.status_label.config(text="PNG to ICO conversion failed", fg="red")
                        self.buttons['compile'].config(state='normal')
                        self.buttons['stop_compile'].config(state='disabled')
                        self._compiling = False
                        return
            data_files = self.data_files.get().strip()
            if data_files:
                for pair in data_files.split(","):
                    pair = pair.strip()
                    if pair:
                        cmd.append(f"--include-data-files={pair}")
            if self.follow_imports.get():
                cmd.append("--follow-imports")
            if self.lto.get():
                cmd.append("--lto")
            if self.clang.get():
                cmd.append("--clang")
            jobs = self.jobs.get()
            if jobs and jobs > 1:
                cmd.append(f"--jobs={jobs}")
            # Output filename
            output_filename = self.output_filename.get().strip()
            if output_filename:
                cmd.append(f"--output-filename={output_filename}")
            # Splash screen option
            splash_img = self.splash_image_path.get().strip()
            splash_timeout = self.splash_timeout.get()
            if splash_img:
                cmd.append(f"--onefile-windows-splash-screen-image={splash_img}")
                if splash_timeout:
                    cmd.append(f"--onefile-windows-splash-screen-timeout={splash_timeout}")
            # Advanced options
            exclude_modules = self.exclude_modules.get().strip()
            if exclude_modules:
                for mod in exclude_modules.split(","):
                    mod = mod.strip()
                    if mod:
                        cmd.append(f"--nofollow-import-to={mod}")
            include_modules = self.include_modules.get().strip()
            if include_modules:
                for mod in include_modules.split(","):
                    mod = mod.strip()
                    if mod:
                        cmd.append(f"--include-module={mod}")
            if self.checkbuttons['remove_output'].cget('variable'):
                if self.checkbuttons['remove_output'].var.get():
                    cmd.append("--remove-output")
            if self.checkbuttons['show_memory'].cget('variable'):
                if self.checkbuttons['show_memory'].var.get():
                    cmd.append("--show-memory")
            if self.checkbuttons['show_progress'].cget('variable'):
                if self.checkbuttons['show_progress'].var.get():
                    cmd.append("--show-progress")
            if self.checkbuttons['pgo'].cget('variable'):
                if self.checkbuttons['pgo'].var.get():
                    cmd.append("--pgo")
            if self.checkbuttons['no_dependency_cache'].cget('variable'):
                if self.checkbuttons['no_dependency_cache'].var.get():
                    cmd.append("--no-dependency-cache")
            compression = self.onefile_compression.get()
            if compression and compression != "auto":
                cmd.append(f"--onefile-compression={compression}")
            python_flags = self.python_flags.get().strip()
            if python_flags:
                for flag in python_flags.split(","):
                    flag = flag.strip()
                    if flag:
                        cmd.append(f"--python-flag={flag}")
            # Custom options
            custom = self.custom_opts.get().strip()
            if custom:
                cmd.extend(custom.split())
            cmd.append(file)
            self.append_log(f"Running: {' '.join(cmd)}\n")
            import subprocess
            self._nuitka_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = self._nuitka_proc.communicate()
            self.append_log(stdout)
            if stderr:
                self.append_log(stderr)
            if self._nuitka_proc.returncode == 0:
                self.status_label.config(text="Compilation succeeded!", fg="green")
            else:
                self.status_label.config(text="Compilation failed. See output.", fg="red")
        except Exception as e:
            self.status_label.config(text="Error running Nuitka.", fg="red")
            self.append_log(str(e))
        finally:
            self.compile_btn.config(state='normal')
            self.buttons['stop_compile'].config(state='disabled')
            self.progress.stop()
            self.progress.grid_remove()
            self._compiling = False

    def append_log(self, text):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, text)
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

    def stop_compiling(self):
        if hasattr(self, '_nuitka_proc') and self._nuitka_proc and self._compiling:
            try:
                self._nuitka_proc.terminate()
                self.append_log('\nCompilation stopped by user.\n')
                self.status_label.config(text="Compilation stopped.", fg="orange")
            except Exception as e:
                self.append_log(f"\nError stopping compilation: {e}\n")
            finally:
                self.buttons['stop_compile'].config(state='disabled')
                self.buttons['compile'].config(state='normal')
                self.progress.stop()
                self.progress.grid_remove()
                self._compiling = False

def main():
    root = tk.Tk()
    app = NuitkaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
