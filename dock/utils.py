import imp
import os
import shutil
import pkg_resources
from tkinter import messagebox
from PIL import ImageTk, Image

HOME_DIR = os.path.expanduser('~')
DEFAULT_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.py")
CONFIG_DIR_PATH = os.path.join(HOME_DIR, ".dock")
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "config.py")

def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        print("Config not found, copying default")
        if not os.path.exists(CONFIG_DIR_PATH):
            os.mkdir(CONFIG_DIR_PATH)
        shutil.copy(DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)
    return imp.load_source('config', CONFIG_FILE_PATH)

def ask_restart_app(root):
    result = messagebox.askyesno("Restart Required", "Program needs to restart for changes to take effect. Do you want to restart?")
    if result != True:
        return
    else:
        root.destroy()
        os.system("dock")

def restore_default_config(root):
    os.remove(CONFIG_FILE_PATH)
    shutil.copy(DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)
    ask_restart_app(root)

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