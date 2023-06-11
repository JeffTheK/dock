def plugin_main(app):
    app.syntax.SUPPORTED_LANGUAGES.append("python")
    app.syntax.FILE_EXTENSIONS["python"] = [".py"]
    app.syntax.KEYWORDS["python"] = [
        "False", "None", "True", "and", "as", "assert",
        "async", "await", "break", "class", "continue",
        "def", "del", "elif", "else", "except", "finally",
        "for", "from", "global", "if", "import", "in", "is",
        "lambda", "nonlocal", "not", "or", "pass", "raise",
        "return", "try", "while", "with", "yield"
    ]
    app.syntax.SEPARATORS["python"] = [' ', '\n', ':', ',', '.']
    app.syntax.BLOCKS["python"] = {
        ('#', '\n'): "green"
    }