# CONFIG VARIABLES

IS_VIM_ENABLED = True

class ROOT:
    TITLE = "Dock"
    GEOMETRY = "800x500"

class CODE_AREA:
    KWARGS = {"row": 0, "column": 1, "sticky": "nsew"}
    
    UNTITLED_BUFFER_NAME = "Untitled"

    BUFFER_BAR_KWARGS = {"height": 20}

    BUFFER_TAB_HIGHLIGHT_COLOR = "white"
    BUFFER_TAB_OPEN_BUTTON_KWARGS = {"cursor": "hand2", "highlightthickness": 0, "borderwidth": 0}
    BUFFER_TAB_CLOSE_BUTTON_KWARGS = {"text": 'x', "cursor": "hand2", "highlightthickness": 0, "borderwidth": 0, "width": 1, "height": 1, "padx": 4, "pady": 0}

    LINE_NUMBERS_KWARGS = {"width": 6, "height": 10}

class STATUS_BAR:
    KWARGS = {"row": 1, "column": 0, "sticky": "nsew"}

class FILE_TREE:
    KWARGS = {"row": 0, "column": 0, "sticky": "nsew"}

# CONFIG FUNCTIONS

def config_root(root):
    root.title(ROOT.TITLE)
    # Set the window size using the geometry method
    root.geometry(ROOT.GEOMETRY)  # Width x Height
    root.grid_rowconfigure(0, weight=1)  # Make the first row of root expand vertically
    root.grid_columnconfigure(0, weight=1)  # Make the first column of root expand horizontally
    root.grid_columnconfigure(1, weight=1)  # Make the first column of root expand horizontally

def config_code_area(code_area):
    code_area.grid(**CODE_AREA.KWARGS)

def config_status_bar(status_bar):
    status_bar.grid(**STATUS_BAR.KWARGS)

def config_file_tree(file_tree):
    file_tree.grid(**FILE_TREE.KWARGS)