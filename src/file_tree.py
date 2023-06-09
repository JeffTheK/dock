import tkinter as tk
from tkinter import ttk
import os

class FileTree(tk.Frame):
    def __init__(self, root, code_area, **kwargs):
        super().__init__(root, **kwargs)
        self.code_area = code_area
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading("#0", text="File Tree", anchor='center')
        self.tree.bind("<Button-1>", self.open_item)
    
    def rebuild(self, path: str):
        self.tree.delete(*self.tree.get_children())
        self.rebuild_recursive(path, "")
    
    def rebuild_recursive(self, directory, parent):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            is_dir = os.path.isdir(item_path)

            item_id = self.tree.insert(parent, "end", text=item, tags=(item_path,))

            if is_dir:
                self.rebuild_recursive(item_path, item_id)
    
    def open_item(self, event):
        from file import open_file
        item = self.tree.selection()
        if item:
            item_text = self.tree.item(item)["text"]
            item_path = self.tree.item(item)["tags"][0]  # Retrieve the full path from the tags
            if not os.path.isfile(item_path):
                return
            open_file(self.code_area, item_path)