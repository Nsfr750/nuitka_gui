import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class CollapsibleSection(ttk.Frame):
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.show = tk.BooleanVar(value=True)
        self.header = ttk.Frame(self)
        self.header.pack(fill="x", expand=False)
        self.toggle_btn = ttk.Button(self.header, width=2, text="-", command=self.toggle, style="Accent.TButton")
        self.toggle_btn.pack(side="left")
        self.label = ttk.Label(self.header, text=title, font=("Segoe UI", 10, "bold"), foreground="#2a4d7a")
        self.label.pack(side="left", padx=4)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
    def toggle(self):
        if self.show.get():
            self.container.forget()
            self.toggle_btn.config(text="+")
        else:
            self.container.pack(fill="both", expand=True)
            self.toggle_btn.config(text="-")
        self.show.set(not self.show.get())

class OptionsPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8, style="Card.TFrame")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#f7faff")
        style.configure("Accent.TButton", foreground="#fff", background="#2a4d7a")
        style.map("Accent.TButton", background=[("active", "#4682b4")])

        # Advanced option variables
        self.disable_console = tk.BooleanVar(value=False)
        self.data_files = tk.StringVar()
        self.follow_imports = tk.BooleanVar(value=False)
        self.lto = tk.BooleanVar(value=False)
        self.clang = tk.BooleanVar(value=False)
        self.jobs = tk.IntVar(value=1)
        self.exclude_modules = tk.StringVar()
        self.include_modules = tk.StringVar()
        self.remove_output = tk.BooleanVar(value=False)
        self.show_memory = tk.BooleanVar(value=False)
        self.show_progress = tk.BooleanVar(value=False)
        self.pgo = tk.BooleanVar(value=False)
        self.no_dependency_cache = tk.BooleanVar(value=False)
        self.onefile_compression = tk.StringVar(value="auto")
        self.python_flags = tk.StringVar()
        self.mingw64 = tk.BooleanVar(value=False)
        self.show_modules = tk.BooleanVar(value=False)
        self.nofollow_import_to = tk.StringVar()
        self.noinclude_module = tk.StringVar()
        self.noinclude_package = tk.StringVar()
        self.assume_yes_for_downloads = tk.BooleanVar(value=False)
        self.windows_uac_admin = tk.BooleanVar(value=False)
        self.windows_uac_uiaccess = tk.BooleanVar(value=False)
        self.windows_company_name = tk.StringVar()
        self.windows_product_name = tk.StringVar()
        self.windows_product_version = tk.StringVar()
        self.windows_file_version = tk.StringVar()
        # Added for requested options
        self.splash_screen_image = tk.StringVar()
        self.plugin_enable = tk.StringVar()
        self.windows_console_mode = tk.StringVar(value="")
        self.icon_from_ico = tk.StringVar()
        self.build_mode = tk.StringVar(value="onefile")  # onefile or standalone
        # Layout (grouped for clarity)
        # --- Build Section ---
        build_sec = CollapsibleSection(self, "Build Mode")
        build_sec.grid(row=0, column=0, sticky="ew", pady=2)
        ttk.Label(build_sec.container, text="Mode:").grid(row=0, column=0, sticky="e", padx=5)
        ttk.Radiobutton(build_sec.container, text="Onefile (--onefile)", variable=self.build_mode, value="onefile").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Radiobutton(build_sec.container, text="Standalone (--standalone)", variable=self.build_mode, value="standalone").grid(row=0, column=2, sticky="w", padx=5)

        win_sec = CollapsibleSection(self, "Windows Executable Options")
        win_sec.grid(row=1, column=0, sticky="ew", pady=2)
        ttk.Label(win_sec.container, text="Splash screen (--onefile-windows-splash-screen-image):").grid(row=0, column=0, sticky="e", padx=5)
        splash_entry = ttk.Entry(win_sec.container, textvariable=self.splash_screen_image, width=25)
        splash_entry.grid(row=0, column=1, sticky="w", padx=5)
        browse_splash_btn = ttk.Button(win_sec.container, text="Browse", command=self.browse_splash_image)
        browse_splash_btn.grid(row=0, column=2, sticky="w", padx=5)
        ttk.Label(win_sec.container, text="Icon from ICO (--windows-icon-from-ico):").grid(row=1, column=0, sticky="e", padx=5)
        icon_entry = ttk.Entry(win_sec.container, textvariable=self.icon_from_ico, width=25)
        icon_entry.grid(row=1, column=1, sticky="w", padx=5)
        browse_icon_btn = ttk.Button(win_sec.container, text="Browse", command=self.browse_icon_ico)
        browse_icon_btn.grid(row=1, column=2, sticky="w", padx=5)
        ttk.Label(win_sec.container, text="Console mode (--windows-console-mode):").grid(row=2, column=0, sticky="e", padx=5)
        ttk.Entry(win_sec.container, textvariable=self.windows_console_mode, width=25).grid(row=2, column=1, sticky="w", padx=5)
        self.check_disable_console = ttk.Checkbutton(win_sec.container, text="Disable console (--windows-disable-console)", variable=self.disable_console)
        self.check_disable_console.grid(row=3, column=0, sticky="w", padx=5, pady=2)

        plugin_sec = CollapsibleSection(self, "Plugins")
        plugin_sec.grid(row=2, column=0, sticky="ew", pady=2)
        ttk.Label(plugin_sec.container, text="Enable plugin (--plugin-enable):").grid(row=0, column=0, sticky="e", padx=5)
        ttk.Entry(plugin_sec.container, textvariable=self.plugin_enable, width=25).grid(row=0, column=1, sticky="w", padx=5)

        data_sec = CollapsibleSection(self, "Data Files")
        data_sec.grid(row=3, column=0, sticky="ew", pady=2)
        ttk.Label(data_sec.container, text="Include data files (--include-data-files):").grid(row=0, column=0, sticky="e", padx=5)
        data_files_entry = ttk.Entry(data_sec.container, textvariable=self.data_files, width=25)
        data_files_entry.grid(row=0, column=1, sticky="w", padx=5)
        browse_data_btn = ttk.Button(data_sec.container, text="Browse", command=self.browse_data_files)
        browse_data_btn.grid(row=0, column=2, sticky="w", padx=5)

        adv_sec = CollapsibleSection(self, "Advanced Options")
        adv_sec.grid(row=4, column=0, sticky="ew", pady=2)
        ttk.Checkbutton(adv_sec.container, text="Follow imports (--follow-imports)", variable=self.follow_imports).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="LTO (--lto)", variable=self.lto).grid(row=0, column=1, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="Clang (--clang)", variable=self.clang).grid(row=0, column=2, sticky="w", padx=5)
        ttk.Label(adv_sec.container, text="Jobs (--jobs):").grid(row=1, column=0, sticky="e", padx=5)
        ttk.Spinbox(adv_sec.container, from_=1, to=16, textvariable=self.jobs, width=5).grid(row=1, column=1, sticky="w", padx=5)
        ttk.Label(adv_sec.container, text="Exclude modules/packages:").grid(row=2, column=0, sticky="e", padx=5)
        ttk.Entry(adv_sec.container, textvariable=self.exclude_modules, width=25).grid(row=2, column=1, sticky="w", padx=5)
        ttk.Label(adv_sec.container, text="Include modules:").grid(row=3, column=0, sticky="e", padx=5)
        ttk.Entry(adv_sec.container, textvariable=self.include_modules, width=25).grid(row=3, column=1, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="Remove output (--remove-output)", variable=self.remove_output).grid(row=4, column=0, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="Show memory (--show-memory)", variable=self.show_memory).grid(row=4, column=1, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="Show progress (--show-progress)", variable=self.show_progress).grid(row=4, column=2, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="PGO (--pgo)", variable=self.pgo).grid(row=5, column=0, sticky="w", padx=5)
        ttk.Checkbutton(adv_sec.container, text="No dependency cache (--no-dependency-cache)", variable=self.no_dependency_cache).grid(row=5, column=1, sticky="w", padx=5)
        ttk.Label(adv_sec.container, text="Onefile compression (use UPX for extra compression):").grid(row=6, column=0, sticky="e", padx=5)
        ttk.OptionMenu(adv_sec.container, self.onefile_compression, "auto", "auto", "upx").grid(row=6, column=1, sticky="w", padx=5)

        rare_sec = CollapsibleSection(adv_sec.container, "Rarely-used Advanced")
        rare_sec.grid(row=7, column=0, columnspan=3, sticky="ew", pady=2, padx=5)
        ttk.Label(rare_sec.container, text="Python flags:").grid(row=0, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.python_flags, width=25).grid(row=0, column=1, sticky="w", padx=5)
        ttk.Checkbutton(rare_sec.container, text="Use MinGW64 (--mingw64)", variable=self.mingw64).grid(row=1, column=0, sticky="w", padx=5)
        ttk.Checkbutton(rare_sec.container, text="Show modules (--show-modules)", variable=self.show_modules).grid(row=1, column=1, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="No follow import to (comma):").grid(row=2, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.nofollow_import_to, width=25).grid(row=2, column=1, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="No include module (comma):").grid(row=3, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.noinclude_module, width=25).grid(row=3, column=1, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="No include package (comma):").grid(row=4, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.noinclude_package, width=25).grid(row=4, column=1, sticky="w", padx=5)
        ttk.Checkbutton(rare_sec.container, text="Assume yes for downloads (--assume-yes-for-downloads)", variable=self.assume_yes_for_downloads).grid(row=5, column=0, sticky="w", padx=5)
        ttk.Checkbutton(rare_sec.container, text="Windows UAC admin (--windows-uac-admin)", variable=self.windows_uac_admin).grid(row=5, column=1, sticky="w", padx=5)
        ttk.Checkbutton(rare_sec.container, text="Windows UAC UIAccess (--windows-uac-uiaccess)", variable=self.windows_uac_uiaccess).grid(row=5, column=2, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="Windows company name:").grid(row=6, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.windows_company_name, width=25).grid(row=6, column=1, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="Windows product name:").grid(row=7, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.windows_product_name, width=25).grid(row=7, column=1, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="Windows product version:").grid(row=8, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.windows_product_version, width=25).grid(row=8, column=1, sticky="w", padx=5)
        ttk.Label(rare_sec.container, text="Windows file version:").grid(row=9, column=0, sticky="e", padx=5)
        ttk.Entry(rare_sec.container, textvariable=self.windows_file_version, width=25).grid(row=9, column=1, sticky="w", padx=5)

    def browse_icon_ico(self):
        file_path = filedialog.askopenfilename(
            title="Select ICO file",
            filetypes=[("ICO files", "*.ico"), ("All files", "*.*")]
        )
        if file_path:
            self.icon_from_ico.set(file_path)

    def browse_splash_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Splash PNG",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.splash_screen_image.set(file_path)

    def browse_data_files(self):
        files = filedialog.askopenfilenames(
            title="Select Data Files",
            filetypes=[("All files", "*.*")]
        )
        if files:
            self.data_files.set(",".join(self.tk.splitlist(files)))
