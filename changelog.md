# Changelog

## v1.4.0 (2025-05-25)
- Added more advanced Nuitka options to the GUI:
  - MinGW64 support
  - UAC admin/UIAccess flags
  - Windows metadata fields (company, product, version)
  - UPX onefile compression
- Grouped advanced options in the GUI for better usability
- Improved error handling and input validation
- Refactored command construction for maintainability
- Enhanced user feedback and status reporting

## v1.3.0 (2025-05-23)
- Added built-in traceback logging (traceback.py)
- Fixed Sponsor dialog modal bugs
- Improved error handling and log viewer integration

## v1.1.0 (2025-05-20)
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
