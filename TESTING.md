# Testing the Terminal Notes Application

## Running Tests Locally

To run the test suite, execute:

```bash
python -m unittest discover -s tests -v
```

Or to run a specific test file:

```bash
python -m unittest tests.test_terminalnotesapp -v
```

## Test Coverage

The test suite covers:

- Note loading and saving functionality
- Note creation, modification, and deletion
- Import and export to JSON files
- Edge cases and error handling
- User input validation
- File handling scenarios

## GitHub Actions

This repository includes GitHub Actions workflow for continuous integration.
See `.github/workflows/test.yml` for details.