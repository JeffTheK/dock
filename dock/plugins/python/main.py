def plugin_main(app):
    app.syntax.SUPPORTED_LANGUAGES.append("python")
    app.syntax.FILE_EXTENSIONS["python"] = [".py"]
    app.syntax.KEYWORDS["python"] = {
        "def": "blue",
        "while": "blue",
        "return": "blue",
        "class": "blue",
        "if": "purple",
        "else": "purple",
        "or": "purple",
        "not": "purple"
    }
    app.syntax.SEPARATORS["python"] = [' ', '\n', ':', ',', '.']
    app.syntax.BLOCKS["python"] = {
        ('#', '\n'): "green"
    }