#!/usr/bin/env bash
# package_linux.sh
# Script to package the terminal notes app into a standalone executable using PyInstaller for Linux/macOS

# Ensure we are in the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH. Please install Python 3.6+."
    exit 1
fi

# Check if PyInstaller is installed; if not, install it
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing via pip..."
    python3 -m pip install --upgrade pyinstaller
    if [[ $? -ne 0 ]]; then
        echo "Failed to install PyInstaller."
        exit 1
    fi
fi

# Build the executable
echo "Building executable with PyInstaller..."
pyinstaller --onefile --name terminalnotesapp main.py
if [[ $? -ne 0 ]]; then
    echo "PyInstaller failed."
    exit 1
fi

echo "Build completed. Executable is in ./dist/terminalnotesapp"
echo "You can distribute the executable from the dist folder."