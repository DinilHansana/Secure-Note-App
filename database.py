import sqlite3

def init_db():
    conn = sqlite3.connect("sakura.db")
    c = conn.cursor()

    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            salt TEXT,
            hashed_pw TEXT,
            twofa_secret TEXT
        )
    """)

    
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            category TEXT DEFAULT 'Personal',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def create_user(username, salt, hashed_pw, twofa_secret):
    conn = sqlite3.connect("sakura.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, salt, hashed_pw, twofa_secret) VALUES (?, ?, ?, ?)",
              (username, salt, hashed_pw, twofa_secret))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect("sakura.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def save_note(user_id, title, encrypted_content, category):
    conn = sqlite3.connect("sakura.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (user_id, title, content, category) VALUES (?, ?, ?, ?)",
              (user_id, title, encrypted_content, category))
    conn.commit()
    conn.close()

def get_notes(user_id):
    conn = sqlite3.connect("sakura.db")
    c = conn.cursor()
    c.execute("SELECT id, title, content, category FROM notes WHERE user_id = ?", (user_id,))
    notes = c.fetchall()
    conn.close()
    return notes

def delete_note(note_id):
    conn = sqlite3.connect("sakura.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
