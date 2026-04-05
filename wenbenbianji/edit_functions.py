"""
编辑功能模块：实现文本编辑的核心逻辑
包括复制、剪切、粘贴、查找、替换等功能
"""

import tkinter as tk
from tkinter import messagebox
import re


class EditFunctions:
    def __init__(self, text_widget, update_status_callback):
        self.text_widget = text_widget
        self.update_status = update_status_callback
        self.last_search = ""
        self.last_replace = ""

    def copy_text(self):
        try:
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_widget.clipboard_clear()
            self.text_widget.clipboard_append(selected_text)
            self.update_status("", "已复制")
        except tk.TclError:
            self.update_status("", "未选中内容")

    def cut_text(self):
        try:
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_widget.clipboard_clear()
            self.text_widget.clipboard_append(selected_text)
            self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.update_status("", "已剪切")
        except tk.TclError:
            self.update_status("", "未选中内容")

    def paste_text(self):
        try:
            clipboard_text = self.text_widget.clipboard_get()
            self.text_widget.insert(tk.INSERT, clipboard_text)
            self.update_status("", "已粘贴")
        except tk.TclError:
            self.update_status("", "剪贴板为空")

    def select_all(self):
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.INSERT, "1.0")
        self.text_widget.focus_set()
        self.update_status("", "已全选")

    def find_text(self):
        search_window = tk.Toplevel()
        search_window.title("查找")
        search_window.geometry("350x150")
        search_window.resizable(False, False)

        tk.Label(search_window, text="查找内容：").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        search_entry = tk.Entry(search_window, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        if self.last_search:
            search_entry.insert(0, self.last_search)
        search_entry.focus_set()

        ignore_case_var = tk.BooleanVar(value=True)
        tk.Checkbutton(search_window, text="忽略大小写", variable=ignore_case_var).grid(
            row=1, column=0, columnspan=2, pady=5
        )

        def perform_search():
            search_text = search_entry.get()
            if not search_text:
                self.update_status("", "请输入查找内容")
                return

            self.last_search = search_text
            self.text_widget.tag_remove("found", "1.0", tk.END)

            content = self.text_widget.get("1.0", tk.END)
            flags = re.IGNORECASE if ignore_case_var.get() else 0

            try:
                matches = list(re.finditer(re.escape(search_text), content, flags))
                if matches:
                    for match in matches:
                        start_pos = match.start()
                        end_pos = match.end()
                        start_index = self._get_index_from_position(content, start_pos)
                        end_index = self._get_index_from_position(content, end_pos)
                        self.text_widget.tag_add("found", start_index, end_index)

                    self.text_widget.tag_config("found", background="yellow")
                    self.text_widget.see(matches[0].start())
                    self.update_status("", f"找到 {len(matches)} 个匹配")
                else:
                    self.update_status("", "无匹配内容")
            except Exception as e:
                self.update_status("", f"查找出错：{str(e)}")

        tk.Button(search_window, text="查找下一个", command=perform_search).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        search_window.transient(self.text_widget.master)
        search_window.grab_set()
        self.text_widget.wait_window(search_window)

    def replace_text(self):
        replace_window = tk.Toplevel()
        replace_window.title("替换")
        replace_window.geometry("400x200")
        replace_window.resizable(False, False)

        tk.Label(replace_window, text="查找内容：").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        search_entry = tk.Entry(replace_window, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        if self.last_search:
            search_entry.insert(0, self.last_search)

        tk.Label(replace_window, text="替换为：").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        replace_entry = tk.Entry(replace_window, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        if self.last_replace:
            replace_entry.insert(0, self.last_replace)

        ignore_case_var = tk.BooleanVar(value=True)
        tk.Checkbutton(replace_window, text="忽略大小写", variable=ignore_case_var).grid(
            row=2, column=0, columnspan=2, pady=5
        )

        def perform_replace_one():
            search_text = search_entry.get()
            replace_text = replace_entry.get()

            if not search_text:
                self.update_status("", "请输入查找内容")
                return

            self.last_search = search_text
            self.last_replace = replace_text

            try:
                selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
                if ignore_case_var.get():
                    if selected_text.lower() == search_text.lower():
                        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                        self.text_widget.insert(tk.INSERT, replace_text)
                        self.update_status("", "已替换")
                    else:
                        self._find_and_select(search_text, ignore_case_var.get())
                else:
                    if selected_text == search_text:
                        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                        self.text_widget.insert(tk.INSERT, replace_text)
                        self.update_status("", "已替换")
                    else:
                        self._find_and_select(search_text, ignore_case_var.get())
            except tk.TclError:
                self._find_and_select(search_text, ignore_case_var.get())

        def perform_replace_all():
            search_text = search_entry.get()
            replace_text = replace_entry.get()

            if not search_text:
                self.update_status("", "请输入查找内容")
                return

            self.last_search = search_text
            self.last_replace = replace_text

            content = self.text_widget.get("1.0", tk.END)
            flags = re.IGNORECASE if ignore_case_var.get() else 0

            try:
                new_content = re.sub(re.escape(search_text), replace_text, content, flags=flags)
                if new_content != content:
                    self.text_widget.delete("1.0", tk.END)
                    self.text_widget.insert("1.0", new_content)
                    count = len(re.findall(re.escape(search_text), content, flags=flags))
                    self.update_status("", f"已替换 {count} 处")
                else:
                    self.update_status("", "无匹配内容")
            except Exception as e:
                self.update_status("", f"替换出错：{str(e)}")

        button_frame = tk.Frame(replace_window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="替换", command=perform_replace_one, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="全部替换", command=perform_replace_all, width=10).pack(side=tk.LEFT, padx=5)

        replace_window.transient(self.text_widget.master)
        replace_window.grab_set()
        self.text_widget.wait_window(replace_window)

    def _find_and_select(self, search_text, ignore_case):
        content = self.text_widget.get("1.0", tk.END)
        flags = re.IGNORECASE if ignore_case else 0

        try:
            match = re.search(re.escape(search_text), content, flags)
            if match:
                start_pos = match.start()
                end_pos = match.end()
                start_index = self._get_index_from_position(content, start_pos)
                end_index = self._get_index_from_position(content, end_pos)

                self.text_widget.tag_remove(tk.SEL, "1.0", tk.END)
                self.text_widget.tag_add(tk.SEL, start_index, end_index)
                self.text_widget.mark_set(tk.INSERT, start_index)
                self.text_widget.focus_set()
                self.text_widget.see(start_index)
                self.update_status("", "找到匹配")
            else:
                self.update_status("", "无匹配内容")
        except Exception as e:
            self.update_status("", f"查找出错：{str(e)}")

    def _get_index_from_position(self, content, position):
        lines_before = content[:position].count('\n')
        chars_in_last_line = position - content.rfind('\n', 0, position) - 1
        return f"{lines_before + 1}.{chars_in_last_line}"

    def apply_syntax_highlight(self, language="python"):
        self.text_widget.tag_remove("keyword", "1.0", tk.END)
        self.text_widget.tag_remove("string", "1.0", tk.END)
        self.text_widget.tag_remove("comment", "1.0", tk.END)

        content = self.text_widget.get("1.0", tk.END)

        if language == "python":
            keywords = ["def", "class", "if", "else", "elif", "for", "while", "try", "except",
                       "finally", "with", "import", "from", "as", "return", "yield", "raise",
                       "pass", "break", "continue", "and", "or", "not", "in", "is", "lambda",
                       "True", "False", "None", "print", "input", "len", "range", "list",
                       "dict", "set", "tuple", "str", "int", "float", "bool"]
            comment_pattern = r'#.*$'
            string_pattern = r'(\".*?\"|\'.*?\')'
        else:
            keywords = ["int", "float", "double", "char", "void", "if", "else", "for",
                       "while", "do", "switch", "case", "break", "continue", "return",
                       "sizeof", "typedef", "struct", "union", "enum", "const", "static",
                       "extern", "volatile", "auto", "register", "signed", "unsigned"]
            comment_pattern = r'//.*$|/\*.*?\*/'
            string_pattern = r'(\".*?\"|\'.*?\')'

        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, content):
                start_idx = self._get_index_from_position(content, match.start())
                end_idx = self._get_index_from_position(content, match.end())
                self.text_widget.tag_add("keyword", start_idx, end_idx)

        for match in re.finditer(string_pattern, content, re.MULTILINE):
            start_idx = self._get_index_from_position(content, match.start())
            end_idx = self._get_index_from_position(content, match.end())
            self.text_widget.tag_add("string", start_idx, end_idx)

        for match in re.finditer(comment_pattern, content, re.MULTILINE):
            start_idx = self._get_index_from_position(content, match.start())
            end_idx = self._get_index_from_position(content, match.end())
            self.text_widget.tag_add("comment", start_idx, end_idx)

        self.text_widget.tag_config("keyword", foreground="blue", font=("Consolas", 12, "bold"))
        self.text_widget.tag_config("string", foreground="green")
        self.text_widget.tag_config("comment", foreground="gray", font=("Consolas", 12, "italic"))
