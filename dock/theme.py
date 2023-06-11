import tkinter as tk

class Theme:
    def __init__(self, name, keyword_color, operator_color, comment_color, string_color, status_bar_bg="", status_bar_text_fg="") -> None:
        self.name = name
        self.keyword_color = keyword_color
        self.operator_color = operator_color
        self.comment_color = comment_color
        self.string_color = string_color
        self.status_bar_bg = status_bar_bg
        self.status_bar_text_fg = status_bar_text_fg

def setup_theme(theme: Theme, app):
    app.current_theme = theme
    app.status_bar.configure(bg=theme.status_bar_bg)
    for child in app.status_bar.winfo_children():
        child.configure(bg=theme.status_bar_bg)
        if isinstance(child, tk.Label):
            child.configure(fg=theme.status_bar_text_fg)