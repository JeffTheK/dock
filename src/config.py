from PIL import ImageTk, Image

def resized_icon(image_path, size):
    # Open the original icon image
    image = Image.open(image_path)

    # Resize the image to the desired dimensions
    resized_image = image.resize(size)

    # Convert the resized image to ImageTk.PhotoImage
    photo_image = ImageTk.PhotoImage(resized_image)

    return photo_image

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
    KWARGS = {"row": 2, "column": 0, "sticky": "nsew", "columnspan": 2}

class FILE_TREE:
    KWARGS = {"row": 0, "column": 0, "sticky": "nsew", "rowspan": 2}
    FILE_ICON = None
    FOLDER_OPEN_ICON = None
    FOLDER_CLOSED_ICON = None

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
    FILE_TREE.FILE_ICON = resized_icon("icon/file.png", (16, 16))
    FILE_TREE.FOLDER_OPEN_ICON = resized_icon("icon/folder_open.png", (16, 16))
    FILE_TREE.FOLDER_CLOSED_ICON = resized_icon("icon/folder_closed.png", (16, 16))

def config_terminal(terminal):
    terminal.grid(**TERMINAL.KWARGS)