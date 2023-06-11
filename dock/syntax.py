from .utils import load_config, merge_instance_variables
from .code_area import CodeArea
from .app import App
from .theme import Theme
import os
import tkinter as tk
import re

config = load_config()

class Syntax:
    pass

def setup_syntax(app: App):
    code_area = app.code_area
    app.syntax = Syntax()
    merge_instance_variables(config.SYNTAX, app.syntax)
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

def highlight_block(text_widget, start_char, end_char, color):
    # Get all text content in the Text widget
    content = text_widget.get("1.0", "end")

    # Find comment sections and apply the tag
    start = "1.0"
    while True:
        start = text_widget.search(start_char, start, "end")
        if not start:
            break

        end = text_widget.search(end_char, f"{start}+1c", "end")
        if start == end:
            break

        if not end:
            end = "end"
        text_widget.tag_add(f"{start_char}{end_char}", start, end)
        start = end

def highlight_words(text_widget, keywords: list, separators: list, theme: Theme):
    text_widget.tag_config("keyword", foreground=theme.keyword_color)
    
    text = text_widget.get("1.0", tk.END)
    lines = text.splitlines(keepends=True)
    for x in range(len(lines)):
        for s in separators:
            lines[x] = lines[x].replace(s, '$')
    line_num = 1
    while line_num <= len(lines):
        line_text = lines[line_num - 1]
        for keyword in keywords:
            word_index = line_text.find(keyword)
            if word_index != -1:
                if (word_index - 1 >= 0) and (line_text[word_index - 1] != '$'):
                    continue
                start = f"{line_num}.{word_index}"
                end = f"{line_num}.{word_index + len(keyword)}"
                #print(keyword + " " + start + ":" + end)
                text_widget.tag_add("keyword", start, end)
        line_num += 1

def clear_tags(code_area: CodeArea):
    all_tags = code_area.input_text.tag_names()
    for tag in all_tags:
        code_area.input_text.tag_delete(tag)

def update_syntax_highlighting(code_area: CodeArea, app: App):
    clear_tags(code_area)

    buffer = code_area.current_buffer
    if buffer is None or buffer.language is None or buffer.language not in app.syntax.SUPPORTED_LANGUAGES:
        return

    highlight_words(code_area.input_text, app.syntax.KEYWORDS[buffer.language], app.syntax.SEPARATORS[buffer.language], app.current_theme)
    for block_chars in app.syntax.BLOCKS[buffer.language].keys():
        color = app.current_theme.comment_color
        code_area.input_text.tag_config(f"{block_chars[0]}{block_chars[1]}", foreground=color)
        highlight_block(code_area.input_text, block_chars[0], block_chars[1], color)

def determine_language_from_extension(extension: str, app: App):
    for lang in app.syntax.SUPPORTED_LANGUAGES:
        if extension in app.syntax.FILE_EXTENSIONS[lang]:
            return lang
    
    return None