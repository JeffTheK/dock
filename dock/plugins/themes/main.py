from dock.theme import Theme

def plugin_main(app):
    app.THEMES["solarized-light"] = Theme(
        name="solarized-light",
        keyword_color="purple",
        operator_color="blue",
        comment_color="green",
        string_color="yellow",
        status_bar_bg="#eee8d5",
        status_bar_text_fg="black",
        code_area_text_bg="#fdf6e3",
        terminal_bg="#fdf6e3",
        file_tree_bg="#eee8d5"
    )