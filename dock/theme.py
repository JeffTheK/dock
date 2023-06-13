import tkinter as tk
from tkinter import ttk

class Theme:
    def __init__(self, name, keyword_color, operator_color, comment_color, string_color, status_bar_bg=None, status_bar_text_fg=None,
        code_area_text_bg=None, code_area_line_numbers_bg=None, terminal_bg=None, file_tree_bg=None
    ) -> None:
        self.name = name
        self.keyword_color = keyword_color
        self.operator_color = operator_color
        self.comment_color = comment_color
        self.string_color = string_color
        self.status_bar_bg = status_bar_bg
        self.status_bar_text_fg = status_bar_text_fg
        self.code_area_text_bg = code_area_text_bg
        self.code_area_line_numbers_bg = code_area_line_numbers_bg
        self.terminal_bg = terminal_bg
        self.file_tree_bg = file_tree_bg

def setup_theme(theme: Theme, app):
    app.style = ttk.Style()

    app.current_theme = theme
    app.status_bar.configure(bg=theme.status_bar_bg)
    for child in app.status_bar.winfo_children():
        child.configure(bg=theme.status_bar_bg)
        if isinstance(child, tk.Label):
            child.configure(fg=theme.status_bar_text_fg)
    
    app.code_area.input_text.configure(bg=theme.code_area_text_bg)
    app.code_area.line_numbers.configure(bg=theme.code_area_line_numbers_bg)

    app.terminal.text.configure(bg=theme.terminal_bg)

    app.style.configure("Custom.Treeview", background=theme.file_tree_bg, 
                fieldbackground=theme.file_tree_bg)
    app.style.configure("Treeview.Heading", background="white", foreground="black")
    app.file_tree.tree.configure(style="Custom.Treeview")