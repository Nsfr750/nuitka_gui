# Nuitka GUI Compiler v1.4.0

A modern Python GUI app to compile Python scripts using Nuitka, with collapsible/expandable option groups, advanced theming, and grouped rarely-used options.

**License:** This project is licensed under the GNU General Public License v3.0 (GPLv3). See LICENSE for details.

## Features
- Select a Python file (*.py) via a file dialog
- Compile it to an executable using Nuitka with one click
- Browse for Windows icon (ICO), splash image (PNG), and data files
- Collapsible/expandable option sections for a clean, focused interface
- Modern themed UI using ttk widgets (ttkbootstrap optional for custom themes)
- Rarely-used options grouped in an "Advanced" section
- Choose Windows icon from ICO, EXE, or PNG files
- PNG icons are automatically converted to ICO (requires Pillow)
- View status and errors in the GUI
- Built-in error logging to Nuitka.log (see traceback.py)
- Log viewer for easy debugging
- Sponsor dialog to support development
- **Advanced Nuitka options:**
  - Exclude/include modules and packages
  - Remove output directory before build
  - Show memory usage and progress
  - Enable PGO (Profile Guided Optimization)
  - Onefile compression (UPX)
  - Python flags
  - MinGW64 support
  - UAC admin/UIAccess flags
  - Windows metadata fields (company, product, version)
  - Grouped advanced options for easier navigation
  - Collapsible "Rarely-used Advanced" section
- Improved error handling and input validation
- Modular codebase for maintainability and extension

## Requirements
- Python 3.x
- Tkinter (comes with standard Python)
- Nuitka (`pip install nuitka`)
- Pillow (`pip install pillow`)  # Only needed for PNG icon support
- ttkbootstrap (`pip install ttkbootstrap`)  # Optional for custom themes

## Usage
1. Run `main.py` with Python:
   ```
   python main.py
   ```
2. Browse for a `.py` file.
3. Browse for icon, splash, and data files as needed.
4. Expand/collapse option sections to focus on what you need.
5. Click "Compile" to build an executable with Nuitka.

The executable will be created in the specified output folder (or the script's folder by default).

## Note
- You must have Nuitka installed and available in your PATH.
- You can customize Nuitka options in the source code if needed.

## License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the LICENSE file for full terms.
