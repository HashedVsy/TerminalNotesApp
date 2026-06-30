# Terminal Notes Application

A simple command-line notes application written in Python with JSON import/export functionality.

## Features

- Create new notes with timestamp-based IDs
- Remove notes by ID
- Modify existing note content
- View all notes with formatted display
- Export notes to JSON file
- Import notes from JSON file (with merge or replace options)
- Cross-platform compatibility (Windows, Linux, macOS)

## Files

- `main.py` - Main application code
- `notes.json` - Data storage file (created automatically)
- `package_linux.sh` - Script to create standalone executable for Linux/macOS using PyInstaller
- `package_win.ps1` - Script to create standalone executable for Windows PowerShell 5.1+ using PyInstaller
- `tests/` - Directory containing unit tests
- `.github/workflows/test.yml` - GitHub Actions workflow for continuous integration

## Getting Started

### Prerequisites

- Python 3.6+ (tested with Python 3.14)
- No external dependencies required (uses only Python standard library)

### Running the Application

```bash
python main.py
```

Follow the on-screen menu to interact with the application.

### Running Tests

```bash
# Discover and run all tests
python -m unittest discover -s tests -v

# Run specific test file
python -m unittest tests.test_terminalnotesapp -v
```

### Creating Executable Bundles

#### Linux/macOS
```bash
bash package_linux.sh
```
The executable will be created in `./dist/terminalnotesapp`

#### Windows (PowerShell 5.1+)
```powershell
powershell -ExecutionPolicy Bypass -File package_win.ps1
```
The executable will be created in `./dist/terminalnotesapp.exe`

## Development

### Project Structure

```
.
├── main.py                 # Main application
├── notes.json              # Data storage (auto-generated)
├── package_linux.sh        # Linux/macOS build script
├── package_win.ps1         # Windows build script
├── tests/                  # Unit tests
│   └── test_terminalnotesapp.py
├── .github/
│   └── workflows/
│       └── test.yml        # GitHub Actions CI/CD
├── TESTING.md              # Testing documentation
└── .gitignore              # Git ignore rules
```

### Testing

The project includes a comprehensive test suite covering:
- Note creation, reading, updating, deletion
- JSON import/export functionality
- Error handling and edge cases
- File I/O operations

To run tests:
```bash
python -m unittest discover -s tests -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is open source and available under the GPLv3 License.

## Acknowledgments

- Built with Python standard library
- Packaging powered by PyInstaller
