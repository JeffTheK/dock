from .utils import load_config
from .code_area import CodeArea
from .app import App
import os
import tkinter as tk
import re

config = load_config()

class Syntax:
    pass

def setup_syntax(app: App):
    code_area = app.code_area
    app.syntax = Syntax()
    config.merge_instance_variables(config.SYNTAX, app.syntax)
    code_area.bind("<<BufferOpened>>", lambda _, c=code_area, a=app: on_buffer_opened(c, a))
    code_area.bind("<<BufferModified>>", lambda _, c=code_area, a=app: update_syntax_highlighting(c, a))

def on_buffer_opened(code_area: CodeArea, app: App):
    if code_area.current_buffer.language is None:
        return

    if code_area.current_buffer.file_path is None:
        return

    _, file_extension = os.path.splitext(code_area.current_buffer.file_path)
    print(file_extension)
    code_area.current_buffer.language = determine_language_from_extension(file_extension, app)
    print(code_area.current_buffer.language)

def highlight_words(text_widget, words_and_colors: dict, separators: list):
    for word, color in words_and_colors.items():
        text_widget.tag_config(word, foreground=color)
    
    text = text_widget.get("1.0", tk.END)
    lines = text.splitlines(keepends=True)
    for x in range(len(lines)):
        for s in separators:
            lines[x] = lines[x].replace(s, '$')
    line_num = 1
    while line_num <= len(lines):
        line_text = lines[line_num - 1]
        for keyword in words_and_colors.keys():
            word_index = line_text.find(keyword)
            if word_index != -1:
                if (word_index - 1 >= 0) and (line_text[word_index - 1] != '$'):
                    continue
                start = f"{line_num}.{word_index}"
                end = f"{line_num}.{word_index + len(keyword)}"
                #print(keyword + " " + start + ":" + end)
                text_widget.tag_add(keyword, start, end)
        line_num += 1

def update_syntax_highlighting(code_area: CodeArea, app: App):
    buffer = code_area.current_buffer
    if buffer is None or buffer.language is None or buffer.language not in config.SYNTAX.SUPPORTED_LANGUAGES:
        return

    highlight_words(code_area.input_text, app.syntax.KEYWORDS[buffer.language], app.syntax.SEPARATORS[buffer.language])

def determine_language_from_extension(extension: str, app: App):
    for lang in app.syntax.SUPPORTED_LANGUAGES:
        if extension in app.syntax.FILE_EXTENSIONS[lang]:
            return lang
    
    return None