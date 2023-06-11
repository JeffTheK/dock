import tkinter as tk
from tkinter import ttk
from .utils import load_config

config = load_config()

class PluginManager(tk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading("#0", text="Plugin Manager", anchor='center')

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        for plugin_name in config.ENABLED_PLUGINS:
            self.tree.insert("", tk.END, text=plugin_name)

    def toggle(self):
        if self.grid_info():
            self.grid_remove()
        else:
            self.grid()
            self.update_tree()