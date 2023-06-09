import tkinter as tk

PAD = 10

class StatusBar(tk.Frame):
    def __init__(self, root, code_area, **kwargs):
        super().__init__(root, **kwargs)
        self.code_area = code_area
        self.pos_label = tk.Label(self, text="Line 0, Col 0")
        self.pos_label.grid(row=0, column=0, padx=PAD)
        self.code_area.input_text.bind("<<Modified>>", self.update, add='+')
        self.code_area.bind("<<AfterCursorMove>>", self.update, add='+')

        self.update()

    def update(self, *args):
        cursor_pos = self.code_area.input_text.index(tk.INSERT)
        print(cursor_pos)
        line, column = cursor_pos.split('.')
        self.pos_label.config(text=f"Line {line}, Column {column}")