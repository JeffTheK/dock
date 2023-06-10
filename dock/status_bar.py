import tkinter as tk

PAD = 10

class StatusBar(tk.Frame):
    def __init__(self, root, code_area, **kwargs):
        super().__init__(root, **kwargs)
        self.code_area = code_area
        self.pos_label = tk.Label(self, text="Line 0, Col 0")
        self.pos_label.grid(row=0, column=0, padx=PAD)
        self.language_label = tk.Label(self, text="No Language")
        self.language_label.grid(row=0, column=2, padx=PAD)
        self.code_area.input_text.bind("<<Modified>>", self.update, add='+')
        self.code_area.bind("<<AfterCursorMove>>", self.update, add='+')

        self.update()
    
    def update(self, *args):
        self.update_cursor_pos()
        self.update_language()
    
    def update_cursor_pos(self):
        cursor_pos = self.code_area.input_text.index(tk.INSERT)
        print(cursor_pos)
        line, column = cursor_pos.split('.')
        self.pos_label.config(text=f"Line {line}, Column {column}")
    
    def update_language(self):
        buffer = self.code_area.current_buffer
        if buffer is None or buffer.language is None:
            self.language_label.config(text=f"No Language")
        else:
            self.language_label.config(text=buffer.language.capitalize())