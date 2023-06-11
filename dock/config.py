from PIL import ImageTk, Image
import pkg_resources
import os

def resized_icon(image_path, size):
    data_dir_path = pkg_resources.resource_filename("dock", '')

    full_path = os.path.join(data_dir_path, image_path)

    # Open the original icon image
    image = Image.open(full_path)

    # Resize the image to the desired dimensions
    resized_image = image.resize(size)

    # Convert the resized image to ImageTk.PhotoImage
    photo_image = ImageTk.PhotoImage(resized_image)

    return photo_image

def merge_instance_variables(source_cls, target_obj):
    for attribute_name in dir(source_cls):
        if not attribute_name.startswith('__'):
            attribute_value = getattr(source_cls, attribute_name)
            setattr(target_obj, attribute_name, attribute_value)

# CONFIG VARIABLES

ENABLED_PLUGINS = ["vim", "python"]
PLUGINS_DIR = pkg_resources.resource_filename("dock", "plugins")

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
    KWARGS = {"row": 2, "column": 0, "sticky": "nsew", "columnspan": 2}

class FILE_TREE:
    KWARGS = {"row": 0, "column": 0, "sticky": "nsew", "rowspan": 2}
    FILE_ICON = None
    FOLDER_OPEN_ICON = None
    FOLDER_CLOSED_ICON = None

class PLUGIN_MANAGER:
    KWARGS = {"row": 0, "column": 0, "sticky": "nsew", "rowspan": 2}

class TERMINAL:
    KWARGS = {"row": 1, "column": 1, "sticky": "nsew"}
    PROMPT = ">>> "

class SYNTAX:
    SUPPORTED_LANGUAGES = ["python"]
    FILE_EXTENSIONS = {"python": [".py"]}
    KEYWORDS = {
        "python": {
            "def": "blue",
            "while": "blue",
            "return": "blue",
            "class": "blue",
            "if": "purple",
            "else": "purple",
            "or": "purple",
            "not": "purple"
        }
    }
    SEPARATORS = {"python": [' ', '\n', ':', ',', '.']}

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
    FILE_TREE.FILE_ICON = resized_icon("data/file.png", (16, 16))
    FILE_TREE.FOLDER_OPEN_ICON = resized_icon("data/folder_open.png", (16, 16))
    FILE_TREE.FOLDER_CLOSED_ICON = resized_icon("data/folder_closed.png", (16, 16))

def config_plugin_manager(plugin_manager):
    plugin_manager.grid(**PLUGIN_MANAGER.KWARGS)
    plugin_manager.toggle()

def config_terminal(terminal):
    terminal.grid(**TERMINAL.KWARGS)