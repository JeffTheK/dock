import imp
import os
import shutil
import pkg_resources
from tkinter import messagebox

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