"""
程序入口：初始化主窗口，加载所有模块，启动事件循环
"""

import tkinter as tk
from tkinter import messagebox
from config import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE
from menu_bar import MenuBar
from tool_bar import ToolBar
from status_bar import StatusBar
from file_operations import FileOperations
from edit_functions import EditFunctions


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("自定义文本编辑器")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self._create_text_widget()
        self._initialize_modules()
        self._bind_events()

    def _create_text_widget(self):
        self.text_widget = tk.Text(
            self.root,
            font=(DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE),
            wrap=tk.NONE,
            undo=True,
            padx=5,
            pady=5
        )
        self.text_widget.pack(expand=True, fill="both")

    def _initialize_modules(self):
        self.status_bar = StatusBar(self.root, self.text_widget)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.file_ops = FileOperations(self.text_widget, self.status_bar.update_status)
        self.edit_funcs = EditFunctions(self.text_widget, self.status_bar.update_status)

        self.tool_bar = ToolBar(self.root, self.text_widget, self.file_ops, self.edit_funcs)
        self.tool_bar.pack(side=tk.TOP, fill=tk.X)

        self.menu_bar = MenuBar(
            self.root,
            self.text_widget,
            self.file_ops,
            self.edit_funcs,
            self.status_bar
        )

    def _bind_events(self):
        self.text_widget.bind("<KeyRelease>", self._on_text_changed)
        self.text_widget.bind("<<Modified>>", self._on_modified)

    def _on_text_changed(self, event):
        pass

    def _on_modified(self, event):
        if self.text_widget.edit_modified():
            self.file_ops.mark_modified()
            self.text_widget.edit_modified(False)

    def on_closing(self):
        if self.file_ops.is_file_modified():
            response = messagebox.askyesnocancel("保存提示", "当前文档已修改，是否保存？")
            if response is True:
                if self.file_ops.save_file():
                    self.root.destroy()
            elif response is False:
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    editor = TextEditor(root)
    root.protocol("WM_DELETE_WINDOW", editor.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
