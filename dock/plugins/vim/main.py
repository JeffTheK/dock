import tkinter as tk
from dock.code_area import CodeArea
from dock.status_bar import StatusBar
from dock.utils import load_config

config = load_config()

def plugin_main(app):
    setup_vim(app.code_area, app.status_bar)

def setup_vim(code_area: CodeArea, status_bar: StatusBar):
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
            if code_area.display_lines_count(index, new_index) == 0:
                code_area.input_text.mark_set(tk.INSERT, new_index)
                code_area.input_text.see(tk.INSERT)
                code_area.event_generate("<<AfterCursorMove>>")
            else:
                lines = code_area.input_text.get("1.0", tk.END).splitlines(keepends=True)
                line1 = lines[int(index.split('.')[0]) - 1]
                y, x = index.split('.')
                endline_index = line1.index('\n')
                new_index = f"{y}.{endline_index}"
                code_area.input_text.mark_set(tk.INSERT, new_index)
                code_area.input_text.see(tk.INSERT)
                code_area.event_generate("<<AfterCursorMove>>")
            return 'break'
        elif event.keysym == 'k':
            # Move Up
            new_index = code_area.input_text.index(f"{index} linestart -1 line")
            if code_area.display_lines_count(index, new_index) == 0:
                code_area.input_text.mark_set(tk.INSERT, new_index)
                code_area.input_text.see(tk.INSERT)
                code_area.event_generate("<<AfterCursorMove>>")
            else:
                lines = code_area.input_text.get("1.0", tk.END).splitlines(keepends=True)
                line1 = lines[int(index.split('.')[0]) - 1]
                y, x = index.split('.')
                endline_index = line1.index('\n')
                new_index = new_index = code_area.input_text.index(f"{index} -{len(line1)} c")
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