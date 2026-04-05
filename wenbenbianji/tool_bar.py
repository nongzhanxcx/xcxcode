"""
工具栏模块：实现快捷工具栏
包含新建、打开、保存、复制、粘贴等常用功能按钮
"""

import tkinter as tk
from tkinter import ttk


class ToolBar:
    def __init__(self, root, text_widget, file_ops, edit_funcs):
        self.root = root
        self.text_widget = text_widget
        self.file_ops = file_ops
        self.edit_funcs = edit_funcs
        self.frame = tk.Frame(root, relief=tk.RAISED, bd=1)
        self._create_buttons()

    def _create_buttons(self):
        button_configs = [
            ("新建", self._new_file),
            ("打开", self._open_file),
            ("保存", self._save_file),
            ("复制", self._copy),
            ("剪切", self._cut),
            ("粘贴", self._paste),
            ("查找", self._find),
            ("替换", self._replace)
        ]

        for text, command in button_configs:
            btn = tk.Button(
                self.frame,
                text=text,
                command=command,
                width=8,
                relief=tk.FLAT,
                padx=5,
                pady=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        self.font_size_var = tk.StringVar(value="12")
        font_label = tk.Label(self.frame, text="字号:")
        font_label.pack(side=tk.LEFT, padx=2)

        font_spinbox = tk.Spinbox(
            self.frame,
            from_=8,
            to=24,
            textvariable=self.font_size_var,
            width=5,
            command=self._change_font_size
        )
        font_spinbox.pack(side=tk.LEFT, padx=2)

        font_spinbox.bind("<Return>", lambda e: self._change_font_size())

        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)

        wrap_var = tk.BooleanVar(value=False)
        wrap_check = tk.Checkbutton(
            self.frame,
            text="自动换行",
            variable=wrap_var,
            command=lambda: self._toggle_wrap(wrap_var.get())
        )
        wrap_check.pack(side=tk.LEFT, padx=5)

        highlight_var = tk.BooleanVar(value=False)
        highlight_check = tk.Checkbutton(
            self.frame,
            text="语法高亮",
            variable=highlight_var,
            command=lambda: self._toggle_highlight(highlight_var.get())
        )
        highlight_check.pack(side=tk.LEFT, padx=5)

    def _new_file(self):
        self.file_ops.new_file()

    def _open_file(self):
        self.file_ops.open_file()

    def _save_file(self):
        self.file_ops.save_file()

    def _copy(self):
        self.edit_funcs.copy_text()

    def _cut(self):
        self.edit_funcs.cut_text()

    def _paste(self):
        self.edit_funcs.paste_text()

    def _find(self):
        self.edit_funcs.find_text()

    def _replace(self):
        self.edit_funcs.replace_text()

    def _change_font_size(self):
        try:
            size = int(self.font_size_var.get())
            if 8 <= size <= 24:
                current_font = self.text_widget.cget("font")
                font_family = current_font[0] if isinstance(current_font, tuple) else "Consolas"
                self.text_widget.config(font=(font_family, size))
        except ValueError:
            pass

    def _toggle_wrap(self, wrap):
        if wrap:
            self.text_widget.config(wrap=tk.WORD)
        else:
            self.text_widget.config(wrap=tk.NONE)

    def _toggle_highlight(self, highlight):
        if highlight:
            self.edit_funcs.apply_syntax_highlight("python")
        else:
            self.text_widget.tag_remove("keyword", "1.0", tk.END)
            self.text_widget.tag_remove("string", "1.0", tk.END)
            self.text_widget.tag_remove("comment", "1.0", tk.END)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_frame(self):
        return self.frame
