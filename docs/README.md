# Nuitka GUI Compiler Documentation

Welcome to the Nuitka GUI Compiler documentation!

## Table of Contents
- Project Overview
- Folder Structure
- Installation
- Usage
- Features
- Development Guide
- Contributing
- License

---

## Project Overview
Nuitka GUI Compiler is a user-friendly graphical interface for compiling Python scripts into standalone executables using Nuitka. It provides advanced options, modern theming, and a modular codebase for easy maintenance and extension.

## Folder Structure
```
├── gui/                # Main GUI components (main window, options panel)
├── struct/             # Modular dialogs and utilities (about, help, log viewer, menu, etc.)
├── docs/               # Project documentation
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── README.md           # Project overview and basic usage
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Nsfr750/nuitka_gui.git
   cd nuitka_gui
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. (Optional) Install Nuitka and any additional compilers as needed.

## Usage
Run the application with:
```sh
python main.py
```
- Use the GUI to select your Python file, configure options, and compile.
- Access Help, About, Log Viewer, and Sponsor dialogs from the menu bar.

## Features
- Compile Python scripts to executables with Nuitka
- Modern themed interface (ttkbootstrap compatible)
- Collapsible/expandable advanced options
- Log viewer and crash report viewer
- Error reporting and feedback dialogs
- Modular, maintainable codebase

## Development Guide
- All dialogs and utilities are in the `struct/` package.
- Main window and UI logic are in the `gui/` package.
- To add new features, create new modules in `struct/` or extend existing ones.
- Ensure new modules are imported using the `struct.` prefix.
- Add an empty `__init__.py` to new package folders.

## Contributing
Contributions are welcome! Please open issues or pull requests for suggestions, bug fixes, or new features.

## License
MIT License. See the main `README.md` for details.
