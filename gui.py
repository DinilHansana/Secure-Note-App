import customtkinter as ctk
from tkinter import messagebox
from auth import hash_password, verify_password, generate_2fa_secret, get_2fa_uri, generate_qr_code, verify_2fa_token
from database import init_db, create_user, get_user, get_notes, save_note, delete_note
from encryption import encrypt_note, decrypt_note
from backup import export_backup, import_backup

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SecureNoteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x500")
        self.title("Secure Note App")
        self.resizable(False, False)
        self.username = None
        self.user_id = None
        self.password = None
        self.current_theme = "light"
        init_db()

        self.login_frame = None
        self.main_frame = None
        self.build_login()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def build_login(self):
        self.clear()

        self.login_frame = ctk.CTkFrame(self, corner_radius=25)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.login_frame.grid_propagate(False)
        self.login_frame.configure(width=620, height=500)

        title = ctk.CTkLabel(self.login_frame, text="Secure Note App", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(10, 20))

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=320)
        self.username_entry.pack(pady=(20, 10))

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=320)
        self.password_entry.pack(pady=(0, 20))

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).pack(pady=(20, 10))
        ctk.CTkButton(self.login_frame, text="Register", command=self.register).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        salt, hashed_pw = hash_password(password)
        twofa_secret = generate_2fa_secret()
        create_user(username, salt, hashed_pw, twofa_secret)

        uri = get_2fa_uri(twofa_secret, username)
        qr_path = generate_qr_code(uri, username)
        messagebox.showinfo("2FA Setup", f"Scan this QR code saved at:\n{qr_path}")
        messagebox.showinfo("Success", "Registered! Now login.")
        self.build_login()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = get_user(username)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        user_id, uname, salt, hashed_pw, twofa_secret = user
        if not verify_password(password, salt, hashed_pw):
            messagebox.showerror("Error", "Wrong password.")
            return

        token = ctk.CTkInputDialog(text="Enter your 2FA Code", title="Two-Factor Authentication").get_input()
        if not verify_2fa_token(twofa_secret, token):
            messagebox.showerror("Error", "Invalid 2FA code.")
            return

        self.username = username
        self.user_id = user_id
        self.password = password
        self.build_main()

    def build_main(self):
        self.clear()

        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.configure(width=700, height=400)

        ctk.CTkLabel(self.main_frame, text=f"Welcome, {self.username}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        search_sort_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_sort_frame.pack(pady=(5, 5))

        self.search_entry = ctk.CTkEntry(search_sort_frame, placeholder_text="Search notes...", width=250)
        self.search_entry.bind("<KeyRelease>", lambda event: self.load_notes())
        self.search_entry.grid(row=0, column=0, padx=5)

        self.sort_option = ctk.CTkOptionMenu(search_sort_frame, values=["Newest", "Oldest", "A-Z", "Z-A"], width=150, command=lambda _: self.load_notes())
        self.sort_option.set("Newest")
        self.sort_option.grid(row=0, column=1, padx=5)

        self.category_filter = ctk.CTkOptionMenu(search_sort_frame, values=["All", "Personal", "Work", "Ideas", "Other"], width=150, command=lambda _: self.load_notes())
        self.category_filter.set("All")
        self.category_filter.grid(row=0, column=2, padx=5)

        self.note_card_frame = ctk.CTkScrollableFrame(self.main_frame, width=600, height=180)
        self.note_card_frame.pack(pady=10, padx=10)

        self.load_notes()

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=15, anchor="center")

        ctk.CTkButton(btn_frame, text="Create Note", command=self.create_note).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="View Note", command=self.view_note).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="Delete Note", command=self.delete_selected_note).grid(row=0, column=2, padx=10)

        action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        action_frame.pack(pady=10, anchor="center")

        ctk.CTkButton(action_frame, text="Backup Notes", command=self.backup_notes).grid(row=0, column=0, padx=10)
        ctk.CTkButton(action_frame, text="Restore Notes", command=self.restore_notes).grid(row=0, column=1, padx=10)

        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_frame.pack(pady=20, anchor="center")

        ctk.CTkButton(bottom_frame, text="Toggle Theme", command=self.toggle_theme).grid(row=0, column=0, padx=10)
        ctk.CTkButton(bottom_frame, text="Logout", command=self.logout).grid(row=0, column=1, padx=10)

    def load_notes(self):
        for widget in self.note_card_frame.winfo_children():
            widget.destroy()

        notes = get_notes(self.user_id)
        category_filter = self.category_filter.get()

        if category_filter != "All":
            notes = [n for n in notes if n[3] == category_filter]

        keyword = self.search_entry.get().strip().lower()
        sort = self.sort_option.get()

        if keyword:
            notes = [n for n in notes if keyword in n[1].lower()]

        if sort == "Newest":
            notes.sort(reverse=True)
        elif sort == "Oldest":
            notes.sort()
        elif sort == "A-Z":
            notes.sort(key=lambda n: n[1].lower())
        elif sort == "Z-A":
            notes.sort(key=lambda n: n[1].lower(), reverse=True)

        self.notes = notes

        for nid, title, encrypted, category in notes:
            card = ctk.CTkFrame(self.note_card_frame, corner_radius=10)
            card.pack(pady=5, fill="x", padx=5)

            ctk.CTkLabel(card, text=f"{title}  [{category}]", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(anchor="w", padx=10, pady=(5, 0))
            preview = decrypt_note(encrypted, self.password)[:100].replace("\n", " ") + "..."
            ctk.CTkLabel(card, text=preview, font=ctk.CTkFont(size=12), anchor="w").pack(anchor="w", padx=10, pady=(0, 5))

            btns = ctk.CTkFrame(card, fg_color="transparent")
            btns.pack(anchor="e", padx=10, pady=(0, 5))
            ctk.CTkButton(btns, text="View", width=80, command=lambda n=nid: self.view_note_by_id(n)).pack(side="left", padx=5)
            ctk.CTkButton(btns, text="Delete", width=80, command=lambda n=nid: self.delete_note_by_id(n)).pack(side="left", padx=5)

    def create_note(self):
        def save():
            title = title_entry.get()
            content = content_box.get("1.0", "end").strip()
            category = category_dropdown.get()
            if title and content:
                encrypted = encrypt_note(content, self.password)
                save_note(self.user_id, title, encrypted, category)
                self.load_notes()
                popup.destroy()

        popup = ctk.CTkToplevel(self)
        popup.title("Create Note")
        popup.geometry("450x400")

        title_entry = ctk.CTkEntry(popup, placeholder_text="Title")
        title_entry.pack(pady=10)

        content_box = ctk.CTkTextbox(popup, height=200)
        content_box.pack(pady=10)

        category_dropdown = ctk.CTkOptionMenu(popup, values=["Personal", "Work", "Ideas", "Other"])
        category_dropdown.set("Personal")
        category_dropdown.pack(pady=10)

        ctk.CTkButton(popup, text="Save", command=save).pack(pady=10)

    def view_note(self):
        messagebox.showinfo("Info", "Please use the View button on each note card.")

    def delete_selected_note(self):
        messagebox.showinfo("Info", "Please use the Delete button on each note card.")

    def view_note_by_id(self, note_id):
        for nid, title, encrypted, _ in self.notes:
            if nid == note_id:
                decrypted = decrypt_note(encrypted, self.password)
                viewer = ctk.CTkToplevel(self)
                viewer.title(f"Viewing: {title}")
                viewer.geometry("500x400")
                ctk.CTkLabel(viewer, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
                text_box = ctk.CTkTextbox(viewer, wrap="word")
                text_box.insert("1.0", decrypted)
                text_box.configure(state="disabled")
                text_box.pack(expand=True, fill="both", padx=15, pady=10)
                return

    def delete_note_by_id(self, note_id):
        delete_note(note_id)
        self.load_notes()

    def toggle_theme(self):
        if self.current_theme == "light":
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.current_theme = "light"

    def backup_notes(self):
        path = export_backup(self.user_id, self.password)
        messagebox.showinfo("Backup Complete", f"Backup saved to:\n{path}")

    def restore_notes(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(title="Select Backup File")
        if not path:
            return
        success = import_backup(self.user_id, self.password, path)
        if success:
            messagebox.showinfo("Success", "Backup restored!")
            self.load_notes()
        else:
            messagebox.showerror("Error", "Restore failed")

    def logout(self):
        self.username = None
        self.user_id = None
        self.password = None
        self.build_login()
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

if __name__ == "__main__":
    app = SecureNoteApp()
    app.mainloop()
