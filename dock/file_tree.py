import tkinter as tk
from tkinter import ttk
from .utils import load_config
import os

config = load_config()

class FileTree(tk.Frame):
    def __init__(self, root, code_area, **kwargs):
        super().__init__(root, **kwargs)
        self.code_area = code_area
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading("#0", text="File Tree", anchor='center')
        self.tree.bind("<<TreeviewSelect>>", self.open_item)
        self.tree.bind("<<TreeviewOpen>>", lambda _: self.update_folder_icon(True), add='+')
        self.tree.bind("<<TreeviewClose>>", lambda _: self.update_folder_icon(False), add='+')
    
    def update_folder_icon(self, is_open: bool):
        item_id = self.tree.selection()
        if is_open:
            self.tree.item(item_id, image=config.FILE_TREE.FOLDER_OPEN_ICON)
        else:
            self.tree.item(item_id, image=config.FILE_TREE.FOLDER_CLOSED_ICON)
    
    def rebuild(self, path: str):
        self.tree.delete(*self.tree.get_children())
        self.rebuild_recursive(path, "")
    
    def rebuild_recursive(self, directory, parent):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            is_dir = os.path.isdir(item_path)

            item_id = self.tree.insert(parent, "end", text=item, tags=(item_path,))


            if is_dir:
                self.tree.item(item_id, image=config.FILE_TREE.FOLDER_CLOSED_ICON)
                self.rebuild_recursive(item_path, item_id)
            else:
                self.tree.item(item_id, image=config.FILE_TREE.FILE_ICON)
    
    def open_item(self, event):
        from .file import open_file
        item = self.tree.selection()
        if item:
            item_text = self.tree.item(item)["text"]
            item_path = self.tree.item(item)["tags"][0]  # Retrieve the full path from the tags
            if os.path.isdir(item_path):
                return
            open_file(self.code_area, item_path)