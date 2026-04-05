"""
状态栏模块：实现状态栏的创建与实时更新
显示光标位置、文档名称、操作状态等信息
"""

import tkinter as tk
from tkinter import ttk


class StatusBar:
    def __init__(self, root, text_widget):
        self.root = root
        self.text_widget = text_widget
        self.frame = tk.Frame(root, relief=tk.SUNKEN, bd=1)
        self.filename_var = tk.StringVar(value="未命名.txt")
        self.position_var = tk.StringVar(value="行 1, 列 1")
        self.status_var = tk.StringVar(value="就绪")

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        filename_label = tk.Label(
            self.frame,
            textvariable=self.filename_var,
            width=30,
            anchor="w",
            padx=5
        )
        filename_label.pack(side=tk.LEFT, padx=5)

        position_label = tk.Label(
            self.frame,
            textvariable=self.position_var,
            width=20,
            anchor="w",
            padx=5
        )
        position_label.pack(side=tk.LEFT, padx=5)

        status_label = tk.Label(
            self.frame,
            textvariable=self.status_var,
            width=30,
            anchor="w",
            padx=5
        )
        status_label.pack(side=tk.LEFT, padx=5)

        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.encoding_var = tk.StringVar(value="UTF-8")
        encoding_label = tk.Label(
            self.frame,
            textvariable=self.encoding_var,
            width=10,
            anchor="w",
            padx=5
        )
        encoding_label.pack(side=tk.LEFT, padx=5)

    def _bind_events(self):
        self.text_widget.bind("<KeyRelease>", self._update_position)
        self.text_widget.bind("<ButtonRelease-1>", self._update_position)
        self.text_widget.bind("<ButtonRelease-3>", self._update_position)

    def _update_position(self, event=None):
        try:
            index = self.text_widget.index(tk.INSERT)
            line, column = index.split(".")
            self.position_var.set(f"行 {line}, 列 {int(column) + 1}")
        except Exception:
            pass

    def update_status(self, filename, status):
        if filename:
            self.filename_var.set(filename)
        if status:
            self.status_var.set(status)

    def update_position(self, line, column):
        self.position_var.set(f"行 {line}, 列 {column}")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_frame(self):
        return self.frame
