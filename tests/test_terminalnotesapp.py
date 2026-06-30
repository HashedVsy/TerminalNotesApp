"""
Test suite for terminal notes application
"""
import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open
import sys

# Add the project root to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


class TestTerminalNotesApp(unittest.TestCase):
    """Test cases for the terminal notes application"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Backup original notes file if it exists
        self.original_notes = "notes.json"
        self.backup_nonexistent = not os.path.exists(self.original_notes)
        if not self.backup_nonexistent:
            with open(self.original_notes, 'r') as f:
                self.original_content = f.read()

        # Create a temporary notes file for testing
        self.test_notes_file = "test_notes.json"
        # Temporarily override the NOTES_FILE constant
        self.original_notes_file = main.NOTES_FILE
        main.NOTES_FILE = self.test_notes_file

    def tearDown(self):
        """Tear down test fixtures after each test method"""
        # Restore original NOTES_FILE
        main.NOTES_FILE = self.original_notes_file

        # Remove test notes file if it exists
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)

        # Restore original notes file if it existed
        if not self.backup_nonexistent:
            with open(self.original_notes, 'w') as f:
                f.write(self.original_content)
        elif os.path.exists(self.original_notes):
            os.remove(self.original_notes)

    def test_load_notes_file_not_exists(self):
        """Test loading notes when file doesn't exist"""
        # Ensure file doesn't exist
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)

        notes = main.load_notes()
        self.assertEqual(notes, [])

    def test_load_notes_file_exists_empty(self):
        """Test loading notes from empty file"""
        with open(self.test_notes_file, 'w') as f:
            f.write('')  # Empty file

        notes = main.load_notes()
        self.assertEqual(notes, [])

    def test_load_notes_file_exists_valid_json(self):
        """Test loading notes from valid JSON file"""
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        with open(self.test_notes_file, 'w') as f:
            json.dump(test_data, f)

        notes = main.load_notes()
        self.assertEqual(notes, test_data)

    def test_load_notes_file_exists_invalid_json(self):
        """Test loading notes from invalid JSON file"""
        with open(self.test_notes_file, 'w') as f:
            f.write('invalid json')

        notes = main.load_notes()
        self.assertEqual(notes, [])

    def test_save_notes(self):
        """Test saving notes to file"""
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        main.save_notes(test_data)

        # Verify file was created with correct content
        self.assertTrue(os.path.exists(self.test_notes_file))
        with open(self.test_notes_file, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, test_data)

    def test_create_note(self):
        """Test creating a new note"""
        # Mock user input
        with patch('builtins.input', return_value='Test note content'):
            with patch('builtins.print'):  # Suppress print output
                main.create_note()

        # Check that note was added
        notes = main.load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['content'], 'Test note content')
        # ID should be a timestamp-based integer
        self.assertIsInstance(notes[0]['id'], int)
        self.assertGreater(notes[0]['id'], 1000000000000)  # Reasonable timestamp

    def test_create_note_empty_content(self):
        """Test creating a note with empty content (should fail)"""
        with patch('builtins.input', return_value=''):
            with patch('builtins.print') as mock_print:
                main.create_note()
                # Check that error message was printed
                printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                self.assertIn('Note cannot be empty', printed_output)

        # No note should be added
        notes = main.load_notes()
        self.assertEqual(len(notes), 0)

    def test_remove_note(self):
        """Test removing a note"""
        # Add test notes
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        main.save_notes(test_data)

        # Mock user input to remove first note
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print'):  # Suppress print output
                main.remove_note()

        # Check that note was removed
        notes = main.load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['id'], 2)
        self.assertEqual(notes[0]['content'], 'Test note 2')

    def test_remove_note_invalid_id(self):
        """Test removing a note with invalid ID"""
        # Add test notes
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        main.save_notes(test_data)

        # Mock user input for non-existent ID
        with patch('builtins.input', return_value='999'):
            with patch('builtins.print') as mock_print:
                main.remove_note()
                # Check that error message was printed
                printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                self.assertIn('No note found with ID 999', printed_output)

        # Notes should remain unchanged
        notes = main.load_notes()
        self.assertEqual(len(notes), 2)

    def test_remove_note_non_numeric_input(self):
        """Test removing a note with non-numeric input"""
        # Add test notes
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        main.save_notes(test_data)

        # Mock user input for non-numeric value
        with patch('builtins.input', return_value='abc'):
            with patch('builtins.print') as mock_print:
                main.remove_note()
                # Check that error message was printed
                printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                self.assertIn('Invalid ID', printed_output)

        # Notes should remain unchanged
        notes = main.load_notes()
        self.assertEqual(len(notes), 2)

    def test_change_note(self):
        """Test changing a note's content"""
        # Add test notes
        test_data = [
            {"id": 1, "content": "Original content"},
            {"id": 2, "content": "Another note"}
        ]
        main.save_notes(test_data)

        # Mock user input: select note 1, then provide new content
        with patch('builtins.input', side_effect=['1', 'Updated content']):
            with patch('builtins.print'):  # Suppress print output
                main.change_note()

        # Check that note was updated
        notes = main.load_notes()
        self.assertEqual(len(notes), 2)
        # Find the note with id=1
        note1 = next(note for note in notes if note['id'] == 1)
        self.assertEqual(note1['content'], 'Updated content')
        # Note with id=2 should be unchanged
        note2 = next(note for note in notes if note['id'] == 2)
        self.assertEqual(note2['content'], 'Another note')

    def test_change_note_empty_content(self):
        """Test changing a note to empty content (should fail)"""
        # Add test notes
        test_data = [
            {"id": 1, "content": "Original content"},
            {"id": 2, "content": "Another note"}
        ]
        main.save_notes(test_data)

        # Mock user input: select note 1, then provide empty content
        with patch('builtins.input', side_effect=['1', '']):
            with patch('builtins.print') as mock_print:
                main.change_note()
                # Check that error message was printed
                printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                self.assertIn('Note cannot be empty', printed_output)

        # Notes should remain unchanged
        notes = main.load_notes()
        self.assertEqual(len(notes), 2)
        note1 = next(note for note in notes if note['id'] == 1)
        self.assertEqual(note1['content'], 'Original content')

    def test_change_note_invalid_id(self):
        """Test changing a note with invalid ID"""
        # Add test notes
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        main.save_notes(test_data)

        # Mock user input for non-existent ID
        with patch('builtins.input', side_effect=['999']):  # Only need first input for ID
            with patch('builtins.print') as mock_print:
                main.change_note()
                # Check that error message was printed
                printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                self.assertIn('No note found with ID 999', printed_output)

        # Notes should remain unchanged
        notes = main.load_notes()
        self.assertEqual(len(notes), 2)

    def test_print_notes_empty(self):
        """Test printing notes when no notes exist"""
        # Ensure no notes file exists
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)

        with patch('builtins.print') as mock_print:
            main.print_notes()
            # Check that appropriate message was printed
            printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
            self.assertIn('No notes found.', printed_output)

    def test_print_notes_with_data(self):
        """Test printing notes when notes exist"""
        test_data = [
            {"id": 1, "content": "Short note"},
            {"id": 2, "content": "This is a longer note that should be truncated in display"}
        ]
        main.save_notes(test_data)

        with patch('builtins.print') as mock_print:
            main.print_notes()
            printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
            # Check for header and content
            self.assertIn('===== YOUR NOTES =====', printed_output)
            self.assertIn('Short note', printed_output)
            self.assertIn('This is a longer note that should be truncated', printed_output)
            # Should show total count
            self.assertIn('Total notes: 2', printed_output)

    def test_export_notes_json(self):
        """Test exporting notes to JSON file"""
        test_data = [
            {"id": 1, "content": "Test note 1"},
            {"id": 2, "content": "Test note 2"}
        ]
        main.save_notes(test_data)

        export_file = "test_export.json"
        try:
            # Mock user input to provide filename
            with patch('builtins.input', return_value=export_file):
                main.export_notes_json()

            # Check if file was created
            self.assertTrue(os.path.exists(export_file))

            # Check content
            with open(export_file, 'r') as f:
                exported_data = json.load(f)

            self.assertEqual(exported_data, test_data)
        finally:
            # Clean up
            if os.path.exists(export_file):
                os.remove(export_file)

    def test_export_notes_json_default_filename(self):
        """Test exporting notes with default filename"""
        test_data = [
            {"id": 1, "content": "Test note 1"}
        ]
        main.save_notes(test_data)

        export_file = "notes_export.json"
        try:
            # Mock user input to accept default (empty string)
            with patch('builtins.input', return_value=''):
                main.export_notes_json()

            # Check if default file was created
            self.assertTrue(os.path.exists(export_file))

            # Check content
            with open(export_file, 'r') as f:
                exported_data = json.load(f)

            self.assertEqual(exported_data, test_data)
        finally:
            # Clean up
            if os.path.exists(export_file):
                os.remove(export_file)

    def test_export_notes_no_notes(self):
        """Test exporting when no notes exist"""
        # Ensure no notes
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)

        with patch('builtins.print') as mock_print:
            main.export_notes_json()
            # Check that appropriate message was printed
            printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
            self.assertIn('No notes to export.', printed_output)

    def test_import_notes_json_replace(self):
        """Test importing notes with replace option"""
        # Set up existing notes
        existing_notes = [
            {"id": 1, "content": "Existing note"}
        ]
        main.save_notes(existing_notes)

        # Create import file
        import_data = [
            {"id": 100, "content": "Imported note 1"},
            {"id": 101, "content": "Imported note 2"}
        ]
        import_file = "test_import.json"
        try:
            with open(import_file, 'w') as f:
                json.dump(import_data, f)

            # Mock input to select replace option and provide filename
            with patch('builtins.input', side_effect=[import_file, 'r']):  # 'r' for replace
                main.import_notes_json()

            # Check that notes were replaced (with new IDs due to conflict avoidance)
            new_notes = main.load_notes()
            self.assertEqual(len(new_notes), 2)
            # Check that content was preserved
            contents = [note['content'] for note in new_notes]
            self.assertIn('Imported note 1', contents)
            self.assertIn('Imported note 2', contents)
            # IDs should be different due to conflict avoidance
            ids = [note['id'] for note in new_notes]
            self.assertNotIn(100, ids)  # Original ID should be changed
            self.assertNotIn(101, ids)  # Original ID should be changed
        finally:
            # Clean up
            if os.path.exists(import_file):
                os.remove(import_file)

    def test_import_notes_json_merge(self):
        """Test importing notes with merge option"""
        # Set up existing notes
        existing_notes = [
            {"id": 1, "content": "Existing note"}
        ]
        main.save_notes(existing_notes)

        # Create import file
        import_data = [
            {"id": 100, "content": "Imported note 1"},
            {"id": 101, "content": "Imported note 2"}
        ]
        import_file = "test_import.json"
        try:
            with open(import_file, 'w') as f:
                json.dump(import_data, f)

            # Mock input to select merge option and provide filename
            with patch('builtins.input', side_effect=[import_file, 'm']):  # 'm' for merge
                main.import_notes_json()

            # Check that notes were merged
            new_notes = main.load_notes()
            self.assertEqual(len(new_notes), 3)  # 1 existing + 2 imported
            # Check that all content is present
            contents = [note['content'] for note in new_notes]
            self.assertIn('Existing note', contents)
            self.assertIn('Imported note 1', contents)
            self.assertIn('Imported note 2', contents)
        finally:
            # Clean up
            if os.path.exists(import_file):
                os.remove(import_file)

    def test_import_notes_json_file_not_found(self):
        """Test importing when file doesn't exist"""
        with patch('builtins.input', return_value='nonexistent.json'):
            with patch('builtins.print') as mock_print:
                main.import_notes_json()
                # Check that error message was printed
                printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                self.assertIn('not found', printed_output)

    def test_import_notes_json_invalid_format(self):
        """Test importing with invalid file format (not a list)"""
        # Create invalid import file (not a list)
        import_file = "test_import.json"
        try:
            with open(import_file, 'w') as f:
                json.dump({"not": "a list"}, f)

            # Mock input to provide filename
            with patch('builtins.input', return_value=import_file):
                with patch('builtins.print') as mock_print:
                    main.import_notes_json()
                    # Check that error message was printed
                    printed_output = ' '.join(str(call) for call in mock_print.call_args_list)
                    self.assertIn('Invalid file format', printed_output)
        finally:
            # Clean up
            if os.path.exists(import_file):
                os.remove(import_file)

    def test_import_notes_json_invalid_entries(self):
        """Test importing with some invalid entries"""
        # Set up existing notes
        existing_notes = [
            {"id": 1, "content": "Existing note"}
        ]
        main.save_notes(existing_notes)

        # Create import file with mix of valid and invalid entries
        import_data = [
            {"id": 100, "content": "Valid note 1"},
            {"id": 101},  # Missing content
            {"content": "Valid note 2"},  # Missing id
            {"id": 102, "content": "Valid note 3"},
            "not a dict",
            None
        ]
        import_file = "test_import.json"
        try:
            with open(import_file, 'w') as f:
                json.dump(import_data, f)

            # Mock input to select merge option and provide filename
            with patch('builtins.input', side_effect=[import_file, 'm']):  # 'm' for merge
                main.import_notes_json()

            # Check that valid notes were imported and invalid ones were skipped
            new_notes = main.load_notes()
            # Should have: 1 existing + 3 valid imported = 4 total
            # The valid entries are: indices 0, 2, 3, 5 (None is skipped, string is skipped, missing content/missing id are skipped)
            # Actually, let's trace through what should be valid:
            # Index 0: {"id": 100, "content": "Valid note 1"} - VALID
            # Index 1: {"id": 101} - INVALID (missing content)
            # Index 2: {"content": "Valid note 2"} - INVALID (missing id)
            # Index 3: {"id": 102, "content": "Valid note 3"} - VALID
            # Index 4: "not a dict" - INVALID (not dict)
            # Index 5: None - INVALID (not dict)
            # So we should have 1 existing + 2 valid = 3 total

            self.assertEqual(len(new_notes), 3)  # 1 existing + 2 valid imported
            contents = [note['content'] for note in new_notes]
            self.assertIn('Existing note', contents)
            self.assertIn('Valid note 1', contents)
            self.assertIn('Valid note 3', contents)
        finally:
            # Clean up
            if os.path.exists(import_file):
                os.remove(import_file)


if __name__ == '__main__':
    unittest.main()