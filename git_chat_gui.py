import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as b
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.constants import *
import requests
import threading
import base64

# Base64 encoded Git icon for embedding
GIT_ICON_B64 = """
R0lGODlhEAAQAPIAAP///wAAAMLCwoKCgpKSkiH5BAEAAAAALAAAAAAQABAAAAIujI+py+0Po5wSgvoOKnuc4eD4nE4JEAoFwF1sA9sAcQSAgLgLde33mK/h7/sDAwA7
"""

class GitCommandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Command Generator")
        self.root.geometry("600x400")
        self.root.minsize(450, 350)

        try:
            icon_data = base64.b64decode(GIT_ICON_B64)
            self.icon = PhotoImage(data=icon_data)
            self.root.iconphoto(True, self.icon)
        except tk.TclError:
            print("Warning: Could not set application icon.")

        # --- Status Bar ---
        # Define status bar first so main_frame can be packed before it
        self.status_var = tk.StringVar()
        status_bar = b.Label(
            self.root,
            textvariable=self.status_var,
            padding=5,
            bootstyle=(PRIMARY, INVERSE)
        )
        status_bar.pack(side=BOTTOM, fill=X)

        # --- Main container ---
        main_frame = b.Frame(self.root, padding=15)
        main_frame.pack(expand=True, fill=BOTH)

        # --- Input Section ---
        input_section_frame = b.Frame(main_frame)
        input_section_frame.pack(fill=X, pady=(0, 10))

        prompt_label = b.Label(input_section_frame, text="Describe what you want to do with Git:")
        prompt_label.pack(fill=X, anchor=W, pady=(0, 5))

        entry_button_frame = b.Frame(input_section_frame)
        entry_button_frame.pack(fill=X)

        self.prompt_entry = b.Entry(entry_button_frame, font=("Helvetica", 11))
        self.prompt_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.prompt_entry.focus()

        self.generate_button = b.Button(
            entry_button_frame,
            text="Generate",
            command=self.start_generation_thread,
            bootstyle=SUCCESS,
        )
        self.generate_button.pack(side=RIGHT)

        # --- Progress Bar ---
        self.progress_bar = b.Progressbar(
            main_frame,
            mode=INDETERMINATE,
            bootstyle=(STRIPED, SUCCESS),
        )

        # --- Output Section ---
        output_label = b.Label(main_frame, text="Generated Git Commands:")
        output_label.pack(fill=X, anchor=W, pady=(5, 5))

        self.result_text = ScrolledText(
            main_frame,
            wrap=WORD,
            font=("Consolas", 10),
            autohide=True,
            padding=10
        )
        self.result_text.pack(expand=True, fill=BOTH)

        self.root.bind('<Return>', lambda event=None: self.generate_button.invoke())
        self.status_var.set("Ready")

    def set_loading_state(self, is_loading):
        """Controls the UI state when generating commands."""
        if is_loading:
            self.generate_button.config(state=DISABLED)
            self.prompt_entry.config(state=DISABLED)
            self.status_var.set("Generating commands...")
            self.progress_bar.pack(fill=X, pady=(0, 5), before=self.result_text)
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.generate_button.config(state=NORMAL)
            self.prompt_entry.config(state=NORMAL)

    def start_generation_thread(self):
        """Validates input and starts the command generation in a separate thread."""
        if not self.prompt_entry.get().strip():
            self.status_var.set("Please enter a description first.")
            return

        self.result_text.delete(1.0, END)
        self.set_loading_state(True)

        thread = threading.Thread(target=self.generate_git_commands)
        thread.daemon = True
        thread.start()

    def generate_git_commands(self):
        """Fetches git commands from the API."""
        prompt = self.prompt_entry.get()
        try:
            response = requests.post(
                "https://www.gitfluence.com/api/generate",
                json={"prompt": prompt},
                timeout=30
            )
            response.raise_for_status()
            commands = response.text.strip()
            self.update_ui(commands, "Commands generated successfully.")

        except requests.exceptions.RequestException as e:
            error_message = f"Error: Could not connect to the API.\n\nDetails: {e}"
            self.update_ui(error_message, "Error")

    def update_ui(self, text, status_text):
        """Schedules UI updates to be run in the main thread."""
        self.root.after(0, self._update_ui_callback, text, status_text)

    def _update_ui_callback(self, text, status_text):
        """The actual UI update logic."""
        self.set_loading_state(False)
        self.result_text.delete(1.0, END)
        self.result_text.insert(END, text)
        self.status_var.set(status_text)


if __name__ == "__main__":
    root = b.Window(themename="litera")
    app = GitCommandApp(root)
    root.mainloop()
