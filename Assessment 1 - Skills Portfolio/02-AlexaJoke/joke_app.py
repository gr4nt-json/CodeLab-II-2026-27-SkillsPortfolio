"""
Alexa Tell Me a Joke Application - Exercise 2
CodeLab II Programming Skills Portfolio

Acknowledgement: The Tkinter grid layout structure and file handling logic 
were developed with the assistance of Qwen (Generative AI). 
Prompt used: "Create a Tkinter class structure that reads a text file line by 
line, splits strings on a specific character, and manages button states."
"""

import tkinter as tk
from tkinter import messagebox
import random
import os

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Tell Me a Joke")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.jokes = []
        self.current_joke = None

        self.load_jokes()

        # UI Layout
        self.title_label = tk.Label(root, text="Alexa, tell me a joke!", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=20)

        self.setup_label = tk.Label(root, text="", font=("Arial", 14), wraplength=450, justify="center")
        self.setup_label.pack(pady=10)

        self.punchline_label = tk.Label(root, text="", font=("Arial", 14, "italic"), wraplength=450, justify="center", fg="blue")
        self.punchline_label.pack(pady=10)

        # Button Frame
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=20)

        self.tell_btn = tk.Button(self.btn_frame, text="Alexa tell me a Joke", command=self.tell_joke, width=20)
        self.tell_btn.grid(row=0, column=0, padx=5, pady=5)

        self.punchline_btn = tk.Button(self.btn_frame, text="Show Punchline", command=self.show_punchline, width=20, state=tk.DISABLED)
        self.punchline_btn.grid(row=0, column=1, padx=5, pady=5)

        self.next_btn = tk.Button(self.btn_frame, text="Next Joke", command=self.next_joke, width=20, state=tk.DISABLED)
        self.next_btn.grid(row=1, column=0, padx=5, pady=5)

        self.quit_btn = tk.Button(self.btn_frame, text="Quit", command=self.quit_app, width=20)
        self.quit_btn.grid(row=1, column=1, padx=5, pady=5)

    def load_jokes(self):
        """Reads the jokes file and splits each line into setup and punchline."""
        file_path = "randomJokes.txt"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    # Split on the first question mark only
                    if '?' in line:
                        setup, punchline = line.split('?', 1)
                        self.jokes.append((setup.strip() + '?', punchline.strip()))
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find '{file_path}'. Please ensure it is in the same folder.")
            self.root.quit()

    def tell_joke(self):
        """Selects a random joke and displays the setup."""
        if not self.jokes:
            return
            
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke[0])
        self.punchline_label.config(text="") # Clear previous punchline
        
        # Update button states
        self.punchline_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.NORMAL)

    def show_punchline(self):
        """Reveals the punchline of the current joke."""
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])
            self.punchline_btn.config(state=tk.DISABLED) # Prevent clicking twice

    def next_joke(self):
        """Requests a new random joke."""
        self.tell_joke()

    def quit_app(self):
        """Closes the application."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()