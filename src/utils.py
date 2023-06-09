import imp
import os

HOME_DIR = os.path.expanduser('~')
CONFIG_PATH = os.path.join(HOME_DIR, ".dock", "config.py")

def load_config():
    return imp.load_source('config', CONFIG_PATH)