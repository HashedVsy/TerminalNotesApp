#!/usr/bin/env pwsh
# package_win.ps1
# Script to package the terminal notes app into a standalone executable using PyInstaller for Windows PowerShell 5.1+

# Ensure we are in the script's directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.6+."
    exit 1
}

# Check if PyInstaller is installed; if not, install it
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing via pip..."
    python -m pip install --upgrade pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install PyInstaller."
        exit 1
    }
}

# Build the executable
Write-Host "Building executable with PyInstaller..."
pyinstaller --onefile --name terminalnotesapp main.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed."
    exit 1
}

Write-Host "Build completed. Executable is in ./dist/terminalnotesapp.exe"
Write-Host "You can distribute the .exe file from the dist folder."