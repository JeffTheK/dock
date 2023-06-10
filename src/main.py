import tkinter as tk
from tkinter import scrolledtext
from code_area import CodeArea
from status_bar import StatusBar
from file_tree import FileTree
from terminal import Terminal
from file import ask_open_file, open_directory, open_file
from vim import setup_vim
from utils import load_config, CONFIG_PATH
from syntax import setup_syntax

config = load_config()

root = tk.Tk()
config.config_root(root)

code_area = CodeArea(root)
config.config_code_area(code_area)

status_bar = StatusBar(root, code_area)
config.config_status_bar(status_bar)

file_tree = FileTree(root, code_area)
config.config_file_tree(file_tree)

terminal = Terminal(root)
config.config_terminal(terminal)

setup_vim(code_area, status_bar)
setup_syntax(code_area)

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New File", command=lambda c=code_area: c.new_buffer())

file_menu.add_command(label="Open File", command=lambda c=code_area: ask_open_file(c))
file_menu.add_command(label="Open Folder", command=lambda f=file_tree: open_directory(f))

file_menu.add_command(label="Save File", command=lambda c=code_area: c.save_current_buffer())

# Create the "Settings" menu
settings_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

settings_menu.add_command(label="Edit Settings", command=lambda c=code_area: open_file(c, CONFIG_PATH))

open_directory(file_tree, ".")

root.eval('tk::PlaceWindow . center')

root.mainloop()
