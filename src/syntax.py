from utils import load_config
from code_area import CodeArea
import os
import tkinter as tk

config = load_config()

def setup_syntax(code_area: CodeArea):
    code_area.bind("<<BufferOpened>>", lambda _, c=code_area: on_buffer_opened(c))
    code_area.bind("<<BufferModified>>", lambda _, c=code_area: update_syntax_highlighting(c))

def on_buffer_opened(code_area: CodeArea):
    if code_area.current_buffer.language is None:
        return

    if code_area.current_buffer.file_path is None:
        return

    _, file_extension = os.path.splitext(code_area.current_buffer.file_path)
    print(file_extension)
    code_area.current_buffer.language = determine_language_from_extension(file_extension)
    print(code_area.current_buffer.language)

def highlight_words(text_widget, words_and_colors: dict, separators: list):
    for word, color in words_and_colors.items():
        text_widget.tag_config(word, foreground=color)
    
    text = text_widget.get("1.0", tk.END)
    lines = text.split('\n')
    line_num = 1
    while line_num < text.count("\n"):
        for word in words_and_colors.keys():
            line_text = lines[line_num - 1]
            position = line_text.find(word)
            if position != -1:
                start = f"{line_num}.{position}"
                end = f"{line_num}.{position + len(word)}"
                print(start)
                text_widget.tag_add(word, start, end)
        line_num += 1

def update_syntax_highlighting(code_area: CodeArea):
    buffer = code_area.current_buffer
    if buffer.language is None or buffer.language not in config.SYNTAX.SUPPORTED_LANGUAGES:
        return

    highlight_words(code_area.input_text, config.SYNTAX.KEYWORDS[buffer.language], config.SYNTAX.SEPARATORS[buffer.language])

def determine_language_from_extension(extension: str):
    for lang in config.SYNTAX.SUPPORTED_LANGUAGES:
        if extension in config.SYNTAX.FILE_EXTENSIONS[lang]:
            return lang
    
    return None