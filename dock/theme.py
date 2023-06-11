class Theme:
    def __init__(self, name, keyword_color, operator_color, comment_color, string_color) -> None:
        self.name = name
        self.keyword_color = keyword_color
        self.operator_color = operator_color
        self.comment_color = comment_color
        self.string_color = string_color

def setup_theme(theme: Theme, app):
    app.current_theme = theme