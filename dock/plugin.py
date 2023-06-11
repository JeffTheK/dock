from .utils import load_config
from .app import App
import os
import imp

config = load_config()

def init_plugins(app: App):
    print("Loading plugins")

    for plugin_name in config.ENABLED_PLUGINS:
        print(f"Loading {plugin_name}... ", end="")
        plugin_dir = os.path.join(config.PLUGINS_DIR, plugin_name)
        entry_file_path = os.path.join(plugin_dir, "main.py")
        plugin = imp.load_source(plugin_name, entry_file_path)
        plugin.plugin_main(app)
        print("done")

    print("All plugins loaded")