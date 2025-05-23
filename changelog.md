# Changelog

## v1.3.0 (2025-05-23)
- Added advanced Nuitka options to the GUI:
  - Exclude/include modules and packages
  - Remove output directory before build
  - Show memory usage and progress
  - Enable PGO (Profile Guided Optimization)
  - Onefile compression selection
  - Python flags and more

## v1.2.0 (2025-05-23)
- Added built-in traceback logging (traceback.py)
- Fixed Sponsor dialog modal bugs
- Improved error handling and log viewer integration

## v1.1.0 (2025-05-23)
- Added support for selecting Windows icons from ICO, EXE, or PNG files.
- PNG icons are automatically converted to ICO using Pillow (if installed).
- Added GUI options for many common Nuitka flags: plugins, data files, jobs, LTO, Clang, follow-imports, and more.
- Improved error handling and user feedback for icon conversion and missing dependencies.
- Updated requirements.txt and README.md to reflect new features and dependencies.

## v1.0.0
- Initial release: GUI for compiling Python scripts with Nuitka.
- Basic options for onefile, standalone, output directory, and custom Nuitka flags.

---
This project is licensed under the GNU General Public License v3.0 (GPLv3). See LICENSE for details.
