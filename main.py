import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import nuitka_traceback as tb_logger
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

        self.remove_output = tk.BooleanVar(value=False)
        self.show_memory = tk.BooleanVar(value=False)
        self.show_progress = tk.BooleanVar(value=False)
        self.pgo = tk.BooleanVar(value=False)
        self.no_dependency_cache = tk.BooleanVar(value=False)

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

        self.build_mode = tk.StringVar(value="onefile")
        self.labels['build_mode'] = tk.Label(root, text="Build mode:")
        self.labels['build_mode'].grid(row=3, column=0, sticky="e", padx=5)
        self.entries['build_mode'] = tk.OptionMenu(root, self.build_mode, "onefile", "standalone", "none")
        self.entries['build_mode'].grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.labels['plugins'] = tk.Label(root, text="--enable-plugin(s):")
        self.labels['plugins'].grid(row=4, column=0, sticky="e", padx=5)
        self.entries['plugins'] = tk.Entry(root, textvariable=self.plugins, width=25)
        self.entries['plugins'].grid(row=4, column=1, sticky="w", padx=5)
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
        self.labels['data_files_hint'] = tk.Label(root, text="pattern=dest (e.g. assets/*=assets/)")
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

        self.checkbuttons['remove_output'] = tk.Checkbutton(root, text="--remove-output", variable=self.remove_output)
        self.checkbuttons['remove_output'].grid(row=10, column=0, sticky="w", padx=5)
        self.checkbuttons['show_memory'] = tk.Checkbutton(root, text="--show-memory", variable=self.show_memory)
        self.checkbuttons['show_memory'].grid(row=10, column=1, sticky="w", padx=5)
        self.checkbuttons['show_progress'] = tk.Checkbutton(root, text="--show-progress", variable=self.show_progress)
        self.checkbuttons['show_progress'].grid(row=10, column=2, sticky="w", padx=5)
        self.checkbuttons['pgo'] = tk.Checkbutton(root, text="--pgo", variable=self.pgo)
        self.checkbuttons['pgo'].grid(row=11, column=0, sticky="w", padx=5)
        self.checkbuttons['no_dependency_cache'] = tk.Checkbutton(root, text="--no-dependency-cache", variable=self.no_dependency_cache)
        self.checkbuttons['no_dependency_cache'].grid(row=11, column=1, sticky="w", padx=5)

        self.labels['onefile_compression'] = tk.Label(root, text="Onefile compression (use UPX for extra compression):")
        self.labels['onefile_compression'].grid(row=12, column=0, sticky="e", padx=5)
        self.onefile_compression = tk.StringVar(value="auto")
        self.entries['onefile_compression'] = tk.OptionMenu(root, self.onefile_compression, "auto", "upx")
        self.entries['onefile_compression'].grid(row=12, column=1, sticky="w", padx=5)

        self.labels['python_flags'] = tk.Label(root, text="Python flags:")
        self.labels['python_flags'].grid(row=13, column=0, sticky="e", padx=5)
        self.python_flags = tk.StringVar()
        self.entries['python_flags'] = tk.Entry(root, textvariable=self.python_flags, width=25)
        self.entries['python_flags'].grid(row=13, column=1, sticky="w", padx=5)
        self.labels['python_flags_hint'] = tk.Label(root, text="comma-separated")
        self.labels['python_flags_hint'].grid(row=13, column=2, sticky="w")

        # --- More Nuitka options ---
        self.mingw64 = tk.BooleanVar(value=False)
        self.checkbuttons['mingw64'] = tk.Checkbutton(root, text="Use MinGW64 (--mingw64)", variable=self.mingw64)
        self.checkbuttons['mingw64'].grid(row=15, column=0, sticky="w", padx=5)

        self.show_modules = tk.BooleanVar(value=False)
        self.checkbuttons['show_modules'] = tk.Checkbutton(root, text="Show modules (--show-modules)", variable=self.show_modules)
        self.checkbuttons['show_modules'].grid(row=15, column=1, sticky="w", padx=5)

        self.nofollow_import_to = tk.StringVar()
        self.labels['nofollow_import_to'] = tk.Label(root, text="No follow import to (comma):")
        self.labels['nofollow_import_to'].grid(row=16, column=0, sticky="e", padx=5)
        self.entries['nofollow_import_to'] = tk.Entry(root, textvariable=self.nofollow_import_to, width=25)
        self.entries['nofollow_import_to'].grid(row=16, column=1, sticky="w", padx=5)

        self.noinclude_module = tk.StringVar()
        self.labels['noinclude_module'] = tk.Label(root, text="No include module (comma):")
        self.labels['noinclude_module'].grid(row=17, column=0, sticky="e", padx=5)
        self.entries['noinclude_module'] = tk.Entry(root, textvariable=self.noinclude_module, width=25)
        self.entries['noinclude_module'].grid(row=17, column=1, sticky="w", padx=5)

        self.noinclude_package = tk.StringVar()
        self.labels['noinclude_package'] = tk.Label(root, text="No include package (comma):")
        self.labels['noinclude_package'].grid(row=18, column=0, sticky="e", padx=5)
        self.entries['noinclude_package'] = tk.Entry(root, textvariable=self.noinclude_package, width=25)
        self.entries['noinclude_package'].grid(row=18, column=1, sticky="w", padx=5)

        self.assume_yes_for_downloads = tk.BooleanVar(value=False)
        self.checkbuttons['assume_yes_for_downloads'] = tk.Checkbutton(root, text="Assume yes for downloads (--assume-yes-for-downloads)", variable=self.assume_yes_for_downloads)
        self.checkbuttons['assume_yes_for_downloads'].grid(row=19, column=0, sticky="w", padx=5)

        self.windows_uac_admin = tk.BooleanVar(value=False)
        self.checkbuttons['windows_uac_admin'] = tk.Checkbutton(root, text="Windows UAC admin (--windows-uac-admin)", variable=self.windows_uac_admin)
        self.checkbuttons['windows_uac_admin'].grid(row=19, column=1, sticky="w", padx=5)

        self.windows_uac_uiaccess = tk.BooleanVar(value=False)
        self.checkbuttons['windows_uac_uiaccess'] = tk.Checkbutton(root, text="Windows UAC UIAccess (--windows-uac-uiaccess)", variable=self.windows_uac_uiaccess)
        self.checkbuttons['windows_uac_uiaccess'].grid(row=19, column=2, sticky="w", padx=5)

        self.labels['windows_company_name'] = tk.Label(root, text="Windows company name:")
        self.labels['windows_company_name'].grid(row=20, column=0, sticky="e", padx=5)
        self.windows_company_name = tk.StringVar()
        self.entries['windows_company_name'] = tk.Entry(root, textvariable=self.windows_company_name, width=25)
        self.entries['windows_company_name'].grid(row=20, column=1, sticky="w", padx=5)

        self.labels['windows_product_name'] = tk.Label(root, text="Windows product name:")
        self.labels['windows_product_name'].grid(row=21, column=0, sticky="e", padx=5)
        self.windows_product_name = tk.StringVar()
        self.entries['windows_product_name'] = tk.Entry(root, textvariable=self.windows_product_name, width=25)
        self.entries['windows_product_name'].grid(row=21, column=1, sticky="w", padx=5)

        self.labels['windows_product_version'] = tk.Label(root, text="Windows product version:")
        self.labels['windows_product_version'].grid(row=22, column=0, sticky="e", padx=5)
        self.windows_product_version = tk.StringVar()
        self.entries['windows_product_version'] = tk.Entry(root, textvariable=self.windows_product_version, width=25)
        self.entries['windows_product_version'].grid(row=22, column=1, sticky="w", padx=5)

        self.labels['windows_file_version'] = tk.Label(root, text="Windows file version:")
        self.labels['windows_file_version'].grid(row=23, column=0, sticky="e", padx=5)
        self.windows_file_version = tk.StringVar()
        self.entries['windows_file_version'] = tk.Entry(root, textvariable=self.windows_file_version, width=25)
        self.entries['windows_file_version'].grid(row=23, column=1, sticky="w", padx=5)

        self.labels['custom_opts'] = tk.Label(root, text="Custom Nuitka options:")
        self.labels['custom_opts'].grid(row=24, column=0, sticky="e", padx=5)
        self.entries['custom_opts'] = tk.Entry(root, textvariable=self.custom_opts, width=40)
        self.entries['custom_opts'].grid(row=24, column=1, columnspan=2, padx=5, pady=5, sticky="we")


    def compile_file(self):
        file = self.file_path.get().strip()
        outdir = self.output_dir.get().strip()
        # --- Input validation ---
        if not file:
            self._show_error("Please select a Python file to compile.")
            messagebox.showerror("Error", "Please select a Python file to compile.")
            return
        if not os.path.isfile(file):
            self._show_error("Selected Python file does not exist.")
            messagebox.showerror("Error", "Selected Python file does not exist.")
            return
        if outdir and not os.path.isdir(outdir):
            self._show_error("Output directory does not exist.")
            messagebox.showerror("Error", "Output directory does not exist.")
            return
        self.progress.grid()
        self.status_label.config(text="Compiling...", fg="blue")
        threading.Thread(target=self.run_nuitka, args=(file, outdir)).start()

    def run_nuitka(self, file, outdir):
        cmd = ["nuitka"]
        # --- Main options ---
        if self.build_mode.get() == "onefile":
            cmd.append("--onefile")
        elif self.build_mode.get() == "standalone":
            cmd.append("--standalone")
        if outdir:
            cmd.append(f"--output-dir={outdir}")
        output_filename = self.output_filename.get().strip()
        if output_filename:
            cmd.append(f"--output-filename={output_filename}")
        icon = self.icon_path.get().strip()
        if icon:
            if self.icon_type.get() == "ico":
                cmd.append(f"--windows-icon-from-ico={icon}")
            elif self.icon_type.get() == "exe":
                cmd.append(f"--windows-icon-from-exe={icon}")
            elif self.icon_type.get() == "png":
                cmd.append(f"--windows-icon-from-png={icon}")
        splash = self.splash_image_path.get().strip()
        if splash:
            cmd.append(f"--windows-splash-screen-image={splash}")
            if self.splash_timeout.get() > 0:
                cmd.append(f"--windows-splash-screen-timeout={self.splash_timeout.get()}")
        if self.disable_console.get():
            cmd.append("--windows-disable-console")
        data_files = self.data_files.get().strip()
        self._append_comma_option(cmd, data_files, "--include-data-files")
        if self.follow_imports.get():
            cmd.append("--follow-imports")
        if self.lto.get():
            cmd.append("--lto")
        if self.clang.get():
            cmd.append("--clang")
        if self.jobs.get() > 1:
            cmd.append(f"--jobs={self.jobs.get()}")
        # Plugins
        plugins = self.plugins.get().strip()
        self._append_comma_option(cmd, plugins, "--enable-plugin")
        # Exclude/include modules
        self._append_comma_option(cmd, self.exclude_modules.get().strip(), "--exclude-module")
        self._append_comma_option(cmd, self.include_modules.get().strip(), "--include-module")
        if self.remove_output.get():
            cmd.append("--remove-output")
        if self.show_memory.get():
            cmd.append("--show-memory")
        if self.show_progress.get():
            cmd.append("--show-progress")
        if self.pgo.get():
            cmd.append("--pgo")
        if self.no_dependency_cache.get():
            cmd.append("--no-dependency-cache")
        compression = self.onefile_compression.get()
        # Nuitka does not support --onefile-compression; offer UPX as an alternative
        if compression == "upx":
            cmd.append("--windows-dependency-tool=upx")
        # 'lzma' is default for onefile in Nuitka, so no extra flag needed. 'none' is not supported.
        python_flags = self.python_flags.get().strip()
        self._append_comma_option(cmd, python_flags, "--python-flag")
        # --- More Nuitka options ---
        if self.mingw64.get():
            cmd.append("--mingw64")
        if self.show_modules.get():
            cmd.append("--show-modules")
        self._append_comma_option(cmd, self.nofollow_import_to.get().strip(), "--nofollow-import-to")
        self._append_comma_option(cmd, self.noinclude_module.get().strip(), "--noinclude-module")
        self._append_comma_option(cmd, self.noinclude_package.get().strip(), "--noinclude-package")
        if self.assume_yes_for_downloads.get():
            cmd.append("--assume-yes-for-downloads")
        if self.windows_uac_admin.get():
            cmd.append("--windows-uac-admin")
        if self.windows_uac_uiaccess.get():
            cmd.append("--windows-uac-uiaccess")
        if self.windows_company_name.get().strip():
            cmd.append(f"--windows-company-name={self.windows_company_name.get().strip()}")
        if self.windows_product_name.get().strip():
            cmd.append(f"--windows-product-name={self.windows_product_name.get().strip()}")
        if self.windows_product_version.get().strip():
            cmd.append(f"--windows-product-version={self.windows_product_version.get().strip()}")
        if self.windows_file_version.get().strip():
            cmd.append(f"--windows-file-version={self.windows_file_version.get().strip()}")
        # Custom options
        custom = self.custom_opts.get().strip()
        if custom:
            cmd.extend(custom.split())
        cmd.append(file)
        self.append_log(f"Running: {' '.join(cmd)}\n")
        import subprocess
        try:
            self._nuitka_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = self._nuitka_proc.communicate()
            self.append_log(stdout)
            if stderr:
                self.append_log(stderr)
            if self._nuitka_proc.returncode == 0:
                self._show_success("Compilation succeeded!")
            else:
                self._show_error("Compilation failed. See output log.")
        except Exception as e:
            self._show_error(f"Error running Nuitka: {e}")
        finally:
            self.buttons['compile'].config(state='normal')
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
