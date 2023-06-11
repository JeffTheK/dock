from .code_area import CodeArea
from .file_tree import FileTree
from .status_bar import StatusBar
from .terminal import Terminal

class App:
    def __init__(self, code_area, file_tree, status_bar, terminal) -> None:
        self.code_area = code_area
        self.file_tree = file_tree
        self.status_bar = status_bar
        self.terminal = terminal