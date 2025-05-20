# 🛡️ SecureNoteApp

SecureNoteApp is a beautifully designed, secure, and offline-first note-taking application built using Python and CustomTkinter. It supports encrypted note storage, 2FA login, dark/light themes, categories, and local backup — all in a clean, modern interface.

This is the Public Repository of the Secure-Note-App. You can either clone this and run (Step by Step Guide below) or use the submitted zip file to get the source code.

GitHub Repository Link:- https://github.com/DinilHansana/Secure-Note-App.git

---

## ✨ Features

- 🔐 AES-256 Encryption for all notes
- 🔒 Two-Factor Authentication (2FA) on login
- 🗂️ Categorize notes: Personal, Work, Ideas, Other
- 🔍 Live search, sort (A–Z, Newest), and category filters
- ✏️ Edit and delete existing notes
- 🌗 Dark and light theme toggle
- 💾 Local backup and restore
- 🖥️ 100% offline — no cloud or internet required

---

## ⚙️ How It Works

1. Register with a username and password
2. Set up 2FA by scanning a QR code in Google Authenticator (or similar)
3. Login using password + 2FA token
4. Create and manage notes — all encrypted using your password
5. Organize notes by category
6. Use search/sort/filter to navigate quickly
7. Backup or restore your data as needed
8. Logout securely when done

---

## 💻 Installation

### 🧩 Prerequisites
- Python 3.10 or higher
- `pip` package manager

---

### 📥 Step-by-step (for **macOS** or **Windows**)

1. **Clone or download** this repo:

```bash
git clone https://github.com/DinilHansana/Secure-Note-App.git
cd SecureNoteApp
```
<br>

2. **Create a Virtual Environment** :

*MacOS/Linux*
```bash
python3 -m venv venv
source venv/bin/activate
```

*Windows*
```bash
python -m venv venv
venv\Scripts\activate
```
<br>

3. **Install dependencies** :

```bash
pip install -r requirements.txt
```
<br>

4. **Run the app** :

```bash
python main.py
```

---

## 🧾 Requirements

```bash
customtkinter
qrcode
pyotp
pillow
```

---

## 📁 Project Structure

```bash
SecureNoteApp/
├── main.py            # Entry point
├── gui.py             # Main UI
├── auth.py            # Login, 2FA, hashing
├── database.py        # SQLite local storage
├── encryption.py      # AES encryption
├── backup.py          # Export/restore logic
├── requirements.txt   # All dependencies
└── README.md
```

---

## 📸 Screenshots

| Login Screen | Dashboard | Dark Mode |
|--------------|-----------|-----------|
| ![](https://i.imgur.com/uELBcL5.png) | ![](https://i.imgur.com/vVoun3d.png) | ![](https://i.imgur.com/60qYFNK.png) |


---

## 👨‍💻 Developer Info

- Author: Hewawasam Hansana

- Platform tested: macOS 15.3, Python 3.12

- Also compatible: Windows 10+, Python 3.10+

---

## 🪪 License

MIT License – free to use and modify.

---
