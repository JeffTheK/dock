import tkinter as tk
from utils import load_config

config = load_config()

class Buffer:
    def __init__(self, text: str, name: str, file_path: str, language: str) -> None:
        self.text = text
        self.name = name
        self.file_path = file_path
        self.language = language
        self.has_unsaved_changes = False
    
    def __eq__(self, __value: object) -> bool:
        return self.file_path == __value.file_path and self.name == __value.name
    
    def __repr__(self) -> str:
        return self.file_path
    
    def __hash__(self) -> int:
        return hash(self.file_path)

class BufferTab(tk.Frame):
    def __init__(self, root, code_area, buffer, **kwargs):
        super().__init__(root, relief="solid", highlightthickness=1, highlightbackground="grey", **kwargs)
        self.buffer = buffer
        self.code_area = code_area
        self.open_button = tk.Button(self, text=buffer.name, command=lambda buf=buffer: self.code_area.open_buffer(buf), **config.CODE_AREA.BUFFER_TAB_OPEN_BUTTON_KWARGS)
        self.open_button.grid(row=0, column=0, sticky="w")
        self.close_button = tk.Button(self, command=lambda: self.code_area.close_buffer(self.buffer), **config.CODE_AREA.BUFFER_TAB_CLOSE_BUTTON_KWARGS)
        self.close_button.grid(row=0, column=1)

        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=0)
    
    def update(self):
        if self.buffer.has_unsaved_changes and not self.open_button.cget("text").startswith("*"):
            self.open_button.config(text=f"*{self.buffer.name}")
    
class BufferBar(tk.Frame):
    def __init__(self, root, code_area, **kwargs):
        super().__init__(root, code_area, **kwargs)
        self.code_area = code_area
        self.tabs = {}
        self.selected_tab = None

    def select_tab(self, buffer: Buffer):
        tab: BufferTab = self.tabs[buffer]
        if self.selected_tab is not None:
            self.selected_tab.open_button.config(fg="grey")
        tab.open_button.config(fg="black")
        self.selected_tab = tab
    
    def add_tab(self, buffer: Buffer):
        tab = BufferTab(self, self.code_area, buffer)
        tab.pack(side="left")
        self.tabs[buffer] = tab
    
    def remove_tab(self, buffer: Buffer):
        tab = self.tabs[buffer]
        if tab == self.selected_tab:
            self.selected_tab = None
        self.tabs.pop(buffer)
        tab.destroy()
    
class CodeArea(tk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.current_buffer = None
        self.buffers = []
        self.buffer_bar = BufferBar(self, self, **config.CODE_AREA.BUFFER_BAR_KWARGS)
        self.buffer_bar.grid(row=0, column=0, columnspan=2, sticky="we")
        self.line_numbers = tk.Text(self, **config.CODE_AREA.LINE_NUMBERS_KWARGS)
        self.line_numbers.grid(row=1, column=0, sticky="nsew")
        self.input_text = tk.Text(self, width=40, height=10, yscrollcommand=self.update_scroll, wrap=tk.CHAR)
        self.scrollbar = tk.Scrollbar(self, command=self.yview)
        self.scrollbar.grid(row=1, column=1, sticky="nes")
        self.input_text.grid(row=1, column=1, sticky="nsew")
        self.input_text.bind("<<Modified>>", self.update_line_numbers)
        self.input_text.bind("<KeyRelease>", self.update_line_highlight)
        self.input_text.bind("<<Modified>>", lambda _: self.event_generate("<<BufferModified>>"), add='+')
        self.bind("<<BufferModified>>", lambda _: setattr(self.current_buffer, "has_unsaved_changes", True), add='+')
        self.bind("<<BufferModified>>", lambda _: self.buffer_bar.selected_tab.update(), add='+')
        self.input_text.bind("<MouseWheel>", self.update_scroll)  # For Windows and macOS
        self.input_text.bind("<Button-5>", self.update_scroll)    # For Linux
        self.input_text.bind("<Configure>", self.update_scroll)
        self.bind("<<AfterCursorMove>>", self.update_line_highlight, add='+')
        self.input_text.bind("<<Modified>>", self.update_line_highlight, add='+')
        self.bind("<Configure>", self.update_line_numbers, add='+')
        self.line_numbers.tag_configure("highlight", background="#cfcfcf")
        self.line_numbers.tag_configure("right_align", justify="right")

        self.grid_rowconfigure(1, weight=1)  # Make the first row expand vertically
        self.grid_columnconfigure(1, weight=1)  # Make the third column expand horizontally

        self.new_buffer()
    
    def clear_input_text(self):
        self.input_text.delete("1.0", "end")
    
    def new_buffer(self):
        buffer = Buffer("", config.CODE_AREA.UNTITLED_BUFFER_NAME, None, None)
        if self.buffers.count(buffer) != 0:
            i = 1
            while self.buffers.count(buffer) != 0:
                buffer.name = f"{config.CODE_AREA.UNTITLED_BUFFER_NAME}-{str(i)}"
                i += 1

        self.open_buffer(buffer)
    
    def open_buffer(self, buffer: Buffer):
        if self.current_buffer is not None and self.current_buffer == buffer:
            return

        if buffer not in self.buffers:
            self.buffers.append(buffer)
            self.buffer_bar.add_tab(buffer)
        if self.current_buffer is not None:
            self.current_buffer.text = self.input_text.get("1.0", tk.END)

        self.current_buffer = buffer
        self.clear_input_text()
        self.input_text.insert("1.0", buffer.text.rstrip("\n"))
        self.input_text.see("1.0")
        self.input_text.mark_set("insert", "1.0")
        self.buffer_bar.select_tab(buffer)
        self.event_generate("<<BufferOpened>>")
    
    def close_buffer(self, buffer: Buffer):
        if self.current_buffer is not None and self.current_buffer == buffer:
            self.current_buffer = None
        self.buffers.remove(buffer)
        self.clear_input_text()
        self.buffer_bar.remove_tab(buffer)
        
        if len(self.buffers) > 0:
            self.open_buffer(self.buffers[-1])
        
    def input_text_line_count(self):
        return self.input_text.count("1.0", tk.END, "displaylines")[0]
    
    def update_line_numbers(self, event):
        self.line_numbers.delete(1.0, tk.END)
        line_count = self.input_text.get(1.0, tk.END).count('\n')
        for x in range(line_count):
            if x == line_count - 1:
                self.line_numbers.insert(tk.END, str(x + 1))
            else:
                display_lines_count = self.input_text.count(f"{x+1}.0", f"{x+1}.end", "displaylines")
                if display_lines_count is not None and display_lines_count[0] > 0:
                    self.line_numbers.insert(tk.END, str(x + 1) + '\n' + ' \n'*display_lines_count[0])
                else:
                    self.line_numbers.insert(tk.END, str(x + 1) + '\n')

        self.line_numbers.tag_add("right_align", "1.0", tk.END)
        self.input_text.edit_modified(False)
        self.update_scroll()
        self.update_line_highlight(None)
    
    def display_lines_count(self, start, end):
        display_lines_count = self.input_text.count(start, end, "displaylines")
        normal_lines_count = int(end.split('.')[0]) - int(start.split('.')[0])
        if display_lines_count is None:
            return 0
        return display_lines_count[0] - normal_lines_count
    
    def update_line_highlight(self, event):
        # Reset the tag before adding it
        self.line_numbers.tag_remove("highlight", "1.0", tk.END)
        cursor_pos = self.input_text.index(tk.INSERT)
        line, column = cursor_pos.split('.')
        display_lines_count = self.display_lines_count(f"1.0", f"{line}.{column}")
        line = int(line) + display_lines_count
        start_index = f"{line}.0"
        end_index = f"{line}.end"
        self.line_numbers.tag_add("highlight", start_index, end_index)

    def yview(self, *args):
        self.input_text.yview(*args)
        self.line_numbers.yview(*args)
        self.scrollbar.set(*args)
    
    def update_scroll(self, *args):
        input_text_scroll = self.input_text.yview()
        line_numbers_scroll = (input_text_scroll[0], input_text_scroll[1])
        self.line_numbers.yview_moveto(str(line_numbers_scroll[0]))
        self.scrollbar.set(*self.input_text.yview())
    
    def save_current_buffer(self):
        from file import save_buffer_to_file

        if self.current_buffer is None:
            return

        save_buffer_to_file(self.current_buffer)