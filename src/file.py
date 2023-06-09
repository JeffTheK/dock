import tkinter as tk
import os
from tkinter import filedialog
from code_area import CodeArea, Buffer
from file_tree import FileTree

def ask_open_file(code_area: CodeArea):
    file_path = filedialog.askopenfilename()
    if file_path == ():
        return

    open_file(code_area, file_path)

def open_file(code_area: CodeArea, file_path: str):
    file = open(file_path, 'r+')
    text = file.read()
    buffer = Buffer(text, os.path.basename(file_path), file_path, 'python')
    code_area.open_buffer(buffer)
    file.close()

def open_directory(file_tree: FileTree):
    path = filedialog.askdirectory()
    if path == "":
        return
    file_tree.rebuild(path)