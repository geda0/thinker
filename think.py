import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import requests
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="URL")
        self.url_label.pack()

        self.url_entry = tk.Entry(self)
        self.url_entry.pack()

        self.hotkey_label = tk.Label(self, text="Hotkey")
        self.hotkey_label.pack()

        self.hotkey_entry = tk.Entry(self)
        self.hotkey_entry.pack()

        self.log_label = tk.Label(self, text="Log")
        self.log_label.pack()

        self.log_text = tk.Text(self)
        self.log_text.pack()

        self.save_button = tk.Button(self, text="SAVE", fg="green", command=self.save_data)
        self.save_button.pack()

    def save_data(self):
        self.url = self.url_entry.get()
        self.hotkey = self.hotkey_entry.get()

        if self.url and self.hotkey:
            messagebox.showinfo("Success", "Data saved successfully!")
            self.start_listener()

    def start_listener(self):
        def on_press(key):
            try:
                if key.char == self.hotkey:
                    # Get the clipboard data
                    clipboard_data = self.master.clipboard_get()
                    response = requests.post(self.url, data = {'data': clipboard_data})

                    # Log the clipboard data and the response
                    self.log_text.insert(tk.END, f'Sent data: {clipboard_data}\n')
                    self.log_text.insert(tk.END, f'Received response: {response.text}\n')
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

root = tk.Tk()
app = Application(master=root)
app.mainloop()