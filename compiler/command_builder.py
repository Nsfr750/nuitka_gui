def build_nuitka_command(main_state, options_state):
    """
    main_state: dict with keys: file_path, output_dir, output_filename, icon_path, icon_type, splash_image_path, splash_timeout
    options_state: dict of all advanced options from OptionsPanel
    Returns: list of command arguments for subprocess
    """
    cmd = ["nuitka"]
    # Main options
    if main_state.get("build_mode") == "onefile":
        cmd.append("--onefile")
    elif main_state.get("build_mode") == "standalone":
        cmd.append("--standalone")
    if main_state.get("output_dir"):
        cmd.append(f"--output-dir={main_state['output_dir']}")
    if main_state.get("output_filename"):
        cmd.append(f"--output-filename={main_state['output_filename']}")
    icon = main_state.get("icon_path", "").strip()
    if icon:
        icon_type = main_state.get("icon_type", "ico")
        if icon_type == "ico":
            cmd.append(f"--windows-icon-from-ico={icon}")
        elif icon_type == "exe":
            cmd.append(f"--windows-icon-from-exe={icon}")
        elif icon_type == "png":
            cmd.append(f"--windows-icon-from-png={icon}")
    splash = main_state.get("splash_image_path", "").strip()
    if splash:
        cmd.append(f"--windows-splash-screen-image={splash}")
        if main_state.get("splash_timeout", 0) > 0:
            cmd.append(f"--windows-splash-screen-timeout={main_state['splash_timeout']}")
    # Advanced options
    if options_state.get("disable_console"):
        cmd.append("--windows-disable-console")
    if options_state.get("data_files"):
        _append_comma_option(cmd, options_state["data_files"], "--include-data-files")
    if options_state.get("follow_imports"):
        cmd.append("--follow-imports")
    if options_state.get("lto"):
        cmd.append("--lto")
    if options_state.get("clang"):
        cmd.append("--clang")
    if options_state.get("jobs", 1) > 1:
        cmd.append(f"--jobs={options_state['jobs']}")
    if options_state.get("plugins"):
        _append_comma_option(cmd, options_state["plugins"], "--enable-plugin")
    _append_comma_option(cmd, options_state.get("exclude_modules", ""), "--exclude-module")
    _append_comma_option(cmd, options_state.get("include_modules", ""), "--include-module")
    if options_state.get("remove_output"):
        cmd.append("--remove-output")
    if options_state.get("show_memory"):
        cmd.append("--show-memory")
    if options_state.get("show_progress"):
        cmd.append("--show-progress")
    if options_state.get("pgo"):
        cmd.append("--pgo")
    if options_state.get("no_dependency_cache"):
        cmd.append("--no-dependency-cache")
    compression = options_state.get("onefile_compression", "auto")
    if compression == "upx":
        cmd.append("--windows-dependency-tool=upx")
    _append_comma_option(cmd, options_state.get("python_flags", ""), "--python-flag")
    if options_state.get("mingw64"):
        cmd.append("--mingw64")
    if options_state.get("show_modules"):
        cmd.append("--show-modules")
    _append_comma_option(cmd, options_state.get("nofollow_import_to", ""), "--nofollow-import-to")
    _append_comma_option(cmd, options_state.get("noinclude_module", ""), "--noinclude-module")
    _append_comma_option(cmd, options_state.get("noinclude_package", ""), "--noinclude-package")
    if options_state.get("assume_yes_for_downloads"):
        cmd.append("--assume-yes-for-downloads")
    if options_state.get("windows_uac_admin"):
        cmd.append("--windows-uac-admin")
    if options_state.get("windows_uac_uiaccess"):
        cmd.append("--windows-uac-uiaccess")
    if options_state.get("windows_company_name"):
        cmd.append(f"--windows-company-name={options_state['windows_company_name']}")
    if options_state.get("windows_product_name"):
        cmd.append(f"--windows-product-name={options_state['windows_product_name']}")
    if options_state.get("windows_product_version"):
        cmd.append(f"--windows-product-version={options_state['windows_product_version']}")
    if options_state.get("windows_file_version"):
        cmd.append(f"--windows-file-version={options_state['windows_file_version']}")
    # Custom options
    if options_state.get("custom_opts"):
        cmd.extend(options_state["custom_opts"].split())
    # File to compile (should be last)
    cmd.append(main_state["file_path"])
    return cmd

def _append_comma_option(cmd, value, flag):
    if value:
        for v in value.split(","):
            v = v.strip()
            if v:
                cmd.append(f"{flag}={v}")
