import tkinter as tk
import subprocess
from .utils import load_config
from tkinter.scrolledtext import ScrolledText

config = load_config()

class Terminal(tk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root)
        self.text = ScrolledText(self, height=10)
        self.text.pack(fill=tk.BOTH)
        self.text.bind('<Key>', self.handle_key, add='+')
        self.print_prompt()
    
    def execute_command(self):
        cursor_position = self.text.index(tk.INSERT)
        cursor_line, cursor_column = cursor_position.split('.')
        command = self.text.get(f"{cursor_line}.{len(config.TERMINAL.PROMPT)}", tk.END)
        if command.replace('\n', '').strip() == "":
            self.text.insert(tk.END, '\n')
            self.print_prompt()
            return
        print("command:", command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        self.text.insert(tk.END, '\n')
        self.text.insert(tk.END, result.stdout)
        self.text.insert(tk.END, result.stderr)
        self.text.see(tk.END)
        self.print_prompt()
    
    def print_prompt(self):
        self.text.insert(self.text.index(tk.INSERT), config.TERMINAL.PROMPT)
    
    def handle_key(self, event):
        print(event.keysym)

        cursor_position = self.text.index(tk.INSERT)
        if cursor_position != self.text.index(tk.END):
            self.text.mark_set(tk.INSERT, tk.END)

        if event.keysym == "Return":
            self.execute_command()
            return "break"
        elif event.keysym == "BackSpace":
            cursor_line, cursor_column = cursor_position.split('.')
            if len(self.text.get(f"{cursor_line}.0", tk.END)) - 1 <= len(config.TERMINAL.PROMPT):
                return "break"

        return None