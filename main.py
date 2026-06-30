import json
import os
import sys
import time

NOTES_FILE = "notes.json"

def load_notes():
    """Load notes from JSON file."""
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_notes(notes):
    """Save notes to JSON file."""
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)


def print_notes():
    """Print all notes."""
    notes = load_notes()
    if not notes:
        print("No notes found.")
        return
    print("\n===== YOUR NOTES =====")
    for note in notes:
        print(f"ID: {note['id']}")
        print(f"Content: {note['content']}")
        print("-" * 40)
    print(f"Total notes: {len(notes)}\n")


def export_notes_json():
    """Export notes to a JSON file."""
    notes = load_notes()
    if not notes:
        print("No notes to export.")
        return
    filename = input("Enter filename to export to (default: notes_export.json): ").strip()
    if not filename:
        filename = "notes_export.json"
    if not filename.endswith('.json'):
        filename += '.json'
    try:
        with open(filename, 'w') as f:
            json.dump(notes, f, indent=2)
        print(f"Notes exported to {filename}")
    except Exception as e:
        print(f"Error exporting notes: {e}")


def import_notes_json():
    """Import notes from a JSON file."""
    filename = input("Enter filename to import from: ").strip()
    if not filename:
        print("No filename provided.")
        return
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return
    try:
        with open(filename, 'r') as f:
            imported_notes = json.load(f)
        if not isinstance(imported_notes, list):
            print("Invalid file format: expected a JSON array.")
            return
        # Validate each entry has id and content
        valid_notes = []
        for i, item in enumerate(imported_notes):
            if not isinstance(item, dict) or 'id' not in item or 'content' not in item:
                print(f"Invalid entry at index {i}: skipping")
                continue
            valid_notes.append(item)
        if not valid_notes:
            print("No valid notes found in file.")
            return
        # Ask user whether to merge or replace
        current_notes = load_notes()
        print(f"Found {len(valid_notes)} valid notes in {filename}")
        print(f"Currently have {len(current_notes)} notes.")
        choice = input("Choose action: (m)erge with existing, (r)eplace existing: ").strip().lower()
        if choice == 'r' or choice == 'replace':
            notes_to_save = valid_notes
            # Reassign IDs to avoid conflicts
            timestamp_base = int(time.time() * 1000)
            for i, note in enumerate(notes_to_save):
                note['id'] = timestamp_base + i
            action = "replaced"
        else:  # merge or any other input
            notes_to_save = current_notes + valid_notes
            # Adjust IDs for imported notes to avoid conflicts
            if current_notes:
                max_id = max(note['id'] for note in current_notes)
                for note in valid_notes:
                    note['id'] = max_id + 1 + valid_notes.index(note)
            action = "merged"
        save_notes(notes_to_save)
        print(f"Notes {action} successfully. Total notes now: {len(notes_to_save)}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in file: {e}")
    except Exception as e:
        print(f"Error importing notes: {e}")

def create_note():
    """Create a new note."""
    notes = load_notes()
    content = input("Enter note content: ").strip()
    if not content:
        print("Note cannot be empty.")
        return
    # Generate a unique ID using current timestamp in milliseconds
    note_id = int(time.time() * 1000)
    notes.append({"id": note_id, "content": content})
    save_notes(notes)
    print(f"Note created with ID {note_id}")

def remove_note():
    """Remove a note by ID."""
    notes = load_notes()
    if not notes:
        print("No notes to remove.")
        return
    print("Select a note to remove:")
    for note in notes:
        content = note['content']
        if len(content) > 50:
            display_content = content[:50] + "..."
        else:
            display_content = content
        print(f"ID: {note['id']} - Content: {display_content}")
    try:
        note_id = int(input("Enter note ID to remove: "))
    except ValueError:
        print("Invalid ID.")
        return
    # Find note with matching ID
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[i]
            save_notes(notes)
            print(f"Note ID {note_id} removed.")
            return
    print(f"No note found with ID {note_id}")

def change_note():
    """Change the content of an existing note."""
    notes = load_notes()
    if not notes:
        print("No notes to change.")
        return
    print("Select a note to change:")
    for note in notes:
        content = note['content']
        if len(content) > 50:
            display_content = content[:50] + "..."
        else:
            display_content = content
        print(f"ID: {note['id']} - Content: {display_content}")
    try:
        note_id = int(input("Enter note ID to change: "))
    except ValueError:
        print("Invalid ID.")
        return
    # Find note with matching ID
    for note in notes:
        if note["id"] == note_id:
            new_content = input("Enter new content: ").strip()
            if not new_content:
                print("Note cannot be empty.")
                return
            note["content"] = new_content
            save_notes(notes)
            print(f"Note ID {note_id} updated.")
            return
    print(f"No note found with ID {note_id}")

def menu():
    print("============")
    print("    MENU    ")
    print("============")
    print("1) Create New Note")
    print("2) Remove Note")
    print("3) Change Note")
    print("4) Print All Notes")
    print("5) Export Notes to JSON")
    print("6) Import Notes from JSON")
    print("7) Exit")

def main():
    while True:
        try:
            menu()
            choice = int(input("Enter one of the choices: "))
            if choice == 1:
                create_note()
            elif choice == 2:
                remove_note()
            elif choice == 3:
                change_note()
            elif choice == 4:
                print_notes()
            elif choice == 5:
                export_notes_json()
            elif choice == 6:
                import_notes_json()
            elif choice == 7:
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("Enter a valid integer!")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()