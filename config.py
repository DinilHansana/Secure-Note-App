import os

APP_NAME = "SecureNoteApp"
DB_NAME = "notes.db"
ENCRYPTION_KEY_LENGTH = 32
PBKDF2_ITERATIONS = 100000
BACKUP_FOLDER = "backups"
QR_FOLDER = "2fa_qr"

# Create necessary folders
os.makedirs(BACKUP_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)
