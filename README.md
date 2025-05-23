# Nuitka GUI Compiler

A simple Python GUI app to compile Python scripts using Nuitka.

**License:** This project is licensed under the GNU General Public License v3.0 (GPLv3). See LICENSE for details.

## Features
- Select a Python file (*.py) via a file dialog
- Compile it to an executable using Nuitka with one click
- Choose Windows icon from ICO, EXE, or PNG files
- PNG icons are automatically converted to ICO (requires Pillow)
- View status and errors in the GUI
- Built-in error logging to Nuitka.log (see traceback.py)
- Log viewer for easy debugging
- Sponsor dialog to support development
- Advanced Nuitka options: exclude/include modules, onefile compression, memory/progress, PGO, python flags, and more

## Requirements
- Python 3.x
- Tkinter (comes with standard Python)
- Nuitka (`pip install nuitka`)
- Pillow (`pip install pillow`)  # Only needed for PNG icon support

## Usage
1. Run `main.py` with Python:
   ```
   python main.py
   ```
2. Browse for a `.py` file.
3. Select your desired icon type (ICO, EXE, or PNG) and browse for the icon file.
   - If you choose PNG, Pillow will convert it to ICO automatically.
4. Click "Compile" to build an executable with Nuitka.

The executable will be created in the specified output folder (or the script's folder by default).

## Note
- You must have Nuitka installed and available in your PATH.
- You can customize Nuitka options in the source code if needed.

## License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the LICENSE file for full terms.
