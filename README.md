# Dock

A text editor made in python using tkinter

## Installation

clone the git repo and run these commands:
```sh
pip install -r requirements.txt
pip install .
```

that's it, you can now run the app using `dock` command

## Configuration

Dock can be configured extensively by modifying `config.py` located in `~/.dock` directory (`~/` is user home directory)

## Plugins

Dock supports plugins made in python. The program will look into `config.PLUGINS_DIR` directory and initializing each plugin 
defined in `config.ENABLED_PLUGINS` by importing `main.py` from plugin root directory and executing `plugin_main(app: App)`.
Currently `config.PLUGINS_DIR` is located in `dock` package folder

### Default Plugins

* Vim - vim like hot keys
* Python - syntax highlighting for python

### Writing a Plugin

1. Create a folder in `config.PLUGINS_DIR` for your plugin, titled with your plugin name, for example `my_plugin`
2. Create a `main.py` inside the plugin folder
3. Write `plugin_main(app: App)` function inside `main`.py
4. Edit `config.ENABLED_PLUGINS` to include your plugin