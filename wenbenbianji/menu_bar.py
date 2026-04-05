"""
菜单栏模块：实现完整的菜单系统
包含文件、编辑、格式、查看、帮助5类菜单
"""

import tkinter as tk
from tkinter import messagebox
from config import (
    WINDOW_TITLE, VERSION, FONT_SIZES, BACKGROUND_COLORS,
    SHORTCUT_KEYS, DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE,
    MIN_FONT_SIZE, MAX_FONT_SIZE, MAX_RECENT_FILES
)


class MenuBar:
    def __init__(self, root, text_widget, file_ops, edit_funcs, status_bar):
        self.root = root
        self.text_widget = text_widget
        self.file_ops = file_ops
        self.edit_funcs = edit_funcs
        self.status_bar = status_bar
        self.current_font_size = DEFAULT_FONT_SIZE
        self.recent_files = []
        self._create_menus()

    def _create_menus(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建", command=self.file_ops.new_file, accelerator=SHORTCUT_KEYS["new"])
        file_menu.add_command(label="打开", command=self.file_ops.open_file, accelerator=SHORTCUT_KEYS["open"])
        file_menu.add_command(label="保存", command=self.file_ops.save_file, accelerator=SHORTCUT_KEYS["save"])
        file_menu.add_command(label="另存为", command=self.file_ops.save_file_as)
        file_menu.add_separator()
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="最近打开", menu=self.recent_menu)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self._exit_app)
        menubar.add_cascade(label="文件", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="撤销", command=self._undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="重做", command=self._redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="复制", command=self.edit_funcs.copy_text, accelerator=SHORTCUT_KEYS["copy"])
        edit_menu.add_command(label="剪切", command=self.edit_funcs.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="粘贴", command=self.edit_funcs.paste_text, accelerator=SHORTCUT_KEYS["paste"])
        edit_menu.add_separator()
        edit_menu.add_command(label="全选", command=self.edit_funcs.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="查找", command=self.edit_funcs.find_text, accelerator=SHORTCUT_KEYS["find"])
        edit_menu.add_command(label="替换", command=self.edit_funcs.replace_text)
        menubar.add_cascade(label="编辑", menu=edit_menu)

        format_menu = tk.Menu(menubar, tearoff=0)
        font_size_menu = tk.Menu(format_menu, tearoff=0)
        for size in FONT_SIZES:
            font_size_menu.add_command(
                label=f"{size}号",
                command=lambda s=size: self._set_font_size(s)
            )
        format_menu.add_cascade(label="字体大小", menu=font_size_menu)

        bg_color_menu = tk.Menu(format_menu, tearoff=0)
        for name, color in BACKGROUND_COLORS.items():
            bg_color_menu.add_command(
                label=name,
                command=lambda c=color: self._set_background_color(c)
            )
        format_menu.add_cascade(label="背景色", menu=bg_color_menu)

        format_menu.add_separator()
        format_menu.add_command(label="Python语法高亮", command=lambda: self.edit_funcs.apply_syntax_highlight("python"))
        format_menu.add_command(label="C语言语法高亮", command=lambda: self.edit_funcs.apply_syntax_highlight("c"))
        format_menu.add_command(label="清除高亮", command=self._clear_highlight)
        menubar.add_cascade(label="格式", menu=format_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="放大", command=self._zoom_in)
        view_menu.add_command(label="缩小", command=self._zoom_out)
        view_menu.add_separator()
        view_menu.add_command(label="自动换行", command=self._toggle_wrap)
        menubar.add_cascade(label="查看", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self._show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)
        self._bind_shortcuts()

    def _bind_shortcuts(self):
        self.root.bind(SHORTCUT_KEYS["new"], lambda e: self.file_ops.new_file())
        self.root.bind(SHORTCUT_KEYS["open"], lambda e: self.file_ops.open_file())
        self.root.bind(SHORTCUT_KEYS["save"], lambda e: self.file_ops.save_file())
        self.root.bind(SHORTCUT_KEYS["copy"], lambda e: self.edit_funcs.copy_text())
        self.root.bind("<Control-x>", lambda e: self.edit_funcs.cut_text())
        self.root.bind(SHORTCUT_KEYS["paste"], lambda e: self.edit_funcs.paste_text())
        self.root.bind(SHORTCUT_KEYS["find"], lambda e: self.edit_funcs.find_text())
        self.root.bind("<Control-a>", lambda e: self.edit_funcs.select_all())
        self.root.bind("<Control-z>", lambda e: self._undo())
        self.root.bind("<Control-y>", lambda e: self._redo())

    def _set_font_size(self, size):
        if MIN_FONT_SIZE <= size <= MAX_FONT_SIZE:
            self.current_font_size = size
            self.text_widget.config(font=(DEFAULT_FONT_FAMILY, size))
            self.status_bar.update_status("", f"字体大小：{size}号")

    def _set_background_color(self, color):
        self.text_widget.config(bg=color)
        self.status_bar.update_status("", "背景色已修改")

    def _zoom_in(self):
        new_size = self.current_font_size + 2
        if new_size <= MAX_FONT_SIZE:
            self._set_font_size(new_size)
        else:
            self.status_bar.update_status("", "已达到最大字体大小")

    def _zoom_out(self):
        new_size = self.current_font_size - 2
        if new_size >= MIN_FONT_SIZE:
            self._set_font_size(new_size)
        else:
            self.status_bar.update_status("", "已达到最小字体大小")

    def _toggle_wrap(self):
        current_wrap = self.text_widget.cget("wrap")
        if current_wrap == tk.NONE:
            self.text_widget.config(wrap=tk.WORD)
            self.status_bar.update_status("", "自动换行：开")
        else:
            self.text_widget.config(wrap=tk.NONE)
            self.status_bar.update_status("", "自动换行：关")

    def _clear_highlight(self):
        self.text_widget.tag_remove("keyword", "1.0", tk.END)
        self.text_widget.tag_remove("string", "1.0", tk.END)
        self.text_widget.tag_remove("comment", "1.0", tk.END)
        self.status_bar.update_status("", "语法高亮已清除")

    def _undo(self):
        try:
            self.text_widget.edit_undo()
            self.status_bar.update_status("", "已撤销")
        except tk.TclError:
            self.status_bar.update_status("", "无法撤销")

    def _redo(self):
        try:
            self.text_widget.edit_redo()
            self.status_bar.update_status("", "已重做")
        except tk.TclError:
            self.status_bar.update_status("", "无法重做")

    def _show_about(self):
        about_text = f"{WINDOW_TITLE}\n\n版本：{VERSION}\n\n基于Python tkinter开发的简易文本编辑器\n支持文本编辑、文件操作、查找替换等功能"
        messagebox.showinfo("关于", about_text)

    def _exit_app(self):
        if self.file_ops.is_file_modified():
            response = messagebox.askyesnocancel("保存提示", "当前文档已修改，是否保存？")
            if response is True:
                if self.file_ops.save_file():
                    self.root.quit()
            elif response is False:
                self.root.quit()
        else:
            self.root.quit()

    def add_recent_file(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        if len(self.recent_files) > MAX_RECENT_FILES:
            self.recent_files = self.recent_files[:MAX_RECENT_FILES]
        self._update_recent_menu()

    def _update_recent_menu(self):
        self.recent_menu.delete(0, tk.END)
        if not self.recent_files:
            self.recent_menu.add_command(label="无最近文件", state=tk.DISABLED)
        else:
            for i, file_path in enumerate(self.recent_files):
                self.recent_menu.add_command(
                    label=f"{i+1}. {file_path}",
                    command=lambda fp=file_path: self._open_recent_file(fp)
                )

    def _open_recent_file(self, file_path):
        self.file_ops.open_file()
