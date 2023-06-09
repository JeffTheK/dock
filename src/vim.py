import tkinter as tk
from code_area import CodeArea
from status_bar import StatusBar
from utils import load_config

config = load_config()

def setup_vim(code_area: CodeArea, status_bar: StatusBar):
    if not config.IS_VIM_ENABLED:
        return

    setup_vim_code_area(code_area)
    setup_vim_status_bar(status_bar, code_area)

def setup_vim_code_area(code_area: CodeArea):
    code_area.input_text.bind('<Key>', lambda event, obj=code_area: handle_key(event, obj), add='+')
    go_normal_mode(code_area)

def setup_vim_status_bar(status_bar: StatusBar, code_area: CodeArea):
    status_bar.mode_label = tk.Label(status_bar, text="-- NORMAL --")
    status_bar.pos_label.grid(row=0, column=1)
    status_bar.mode_label.grid(row=0, column=0)
    code_area.bind("<<ModeChange>>", lambda event, sbar=status_bar, carea=code_area: update_status_bar_mode(sbar, carea))

def update_status_bar_mode(status_bar: StatusBar, code_area: CodeArea):
    status_bar.mode_label.config(text=f"-- {code_area.mode.upper()} --")

def go_normal_mode(code_area: CodeArea):
    print("normal")
    code_area.mode = "normal"
    code_area.event_generate("<<ModeChange>>")

def go_insert_mode(code_area: CodeArea):
    print("insert")
    code_area.mode = "insert"
    code_area.event_generate("<<ModeChange>>")

def handle_key(event, code_area: CodeArea):
    # Get the current cursor position
    index = code_area.input_text.index(tk.INSERT)
    print(event.keysym)

    if (code_area.mode == "normal"):
        if event.keysym == 'i':
            # Enter insert mode
            go_insert_mode(code_area)
            return 'break'  # Prevent default behavior
        elif event.keysym == 'h':
            # Move left
            code_area.input_text.mark_set(tk.INSERT, f"{index}-1c")
            code_area.event_generate("<<AfterCursorMove>>")
            return 'break'  # Prevent default behavior
    
        elif event.keysym == 'l':
            # Move right
            code_area.input_text.mark_set(tk.INSERT, f"{index}+1c")
            code_area.event_generate("<<AfterCursorMove>>")
            return 'break'  # Prevent default behavior
        elif event.keysym == 'j':
            # Move Down
            new_index = code_area.input_text.index(f"{index} linestart +1 line")
            code_area.input_text.mark_set(tk.INSERT, new_index)
            code_area.input_text.see(tk.INSERT)
            code_area.event_generate("<<AfterCursorMove>>")
            return 'break'
        elif event.keysym == 'k':
            # Move Up
            new_index = code_area.input_text.index(f"{index} linestart -1 line")
            code_area.input_text.mark_set(tk.INSERT, new_index)
            code_area.input_text.see(tk.INSERT)
            code_area.event_generate("<<AfterCursorMove>>")
            return 'break'
        else:
            return 'break'
    elif (code_area.mode == "insert"):
        if event.keysym == 'Escape':
            # Exit insert mode
            go_normal_mode(code_area)
            return 'break'  # Prevent default behavior
    
    # Handle other keybindings here
    
    # If the key was not handled, allow default behavior
    return None