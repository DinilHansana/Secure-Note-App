import os
import json
from config import BACKUP_FOLDER
from database import get_notes, save_note
from encryption import encrypt_note, decrypt_note

def export_backup(user_id, password, filename="secure_notes_backup.json"):
    notes = get_notes(user_id)
    backup_data = []

    for note_id, title, encrypted_content in notes:
        decrypted = decrypt_note(encrypted_content, password)
        backup_data.append({"title": title, "content": decrypted})

    json_string = json.dumps(backup_data)
    encrypted = encrypt_note(json_string, password)

    path = os.path.join(BACKUP_FOLDER, filename)
    with open(path, "w") as f:
        f.write(encrypted)

    return path

def import_backup(user_id, password, filepath):
    try:
        with open(filepath, "r") as f:
            encrypted_data = f.read()

        decrypted_json = decrypt_note(encrypted_data, password)
        notes = json.loads(decrypted_json)

        for note in notes:
            title = note.get("title")
            content = note.get("content")
            encrypted = encrypt_note(content, password)
            save_note(user_id, title, encrypted)

        return True
    except Exception as e:
        print("Restore error:", e)
        return False
