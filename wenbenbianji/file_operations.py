"""
文件操作模块：实现文件的打开、保存、另存为功能
包含异常处理和文件路径管理
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os


class FileOperations:
    def __init__(self, text_widget, update_status_callback):
        self.text_widget = text_widget
        self.update_status = update_status_callback
        self.current_file = None
        self.is_modified = False

    def new_file(self):
        try:
            if self.is_modified:
                response = messagebox.askyesnocancel("保存提示", "当前文档已修改，是否保存？")
                if response is True:
                    if not self.save_file():
                        return
                elif response is None:
                    return

            self.text_widget.delete(1.0, tk.END)
            self.current_file = None
            self.is_modified = False
            self.update_status("未命名.txt", "新建文档")
            return True
        except Exception as e:
            messagebox.showerror("错误", f"新建文档失败：{str(e)}")
            return False

    def open_file(self):
        try:
            if self.is_modified:
                response = messagebox.askyesnocancel("保存提示", "当前文档已修改，是否保存？")
                if response is True:
                    if not self.save_file():
                        return
                elif response is None:
                    return

            file_path = filedialog.askopenfilename(
                title="打开文件",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )

            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.text_widget.delete(1.0, tk.END)
                    self.text_widget.insert(1.0, content)
                    self.current_file = file_path
                    self.is_modified = False
                    filename = os.path.basename(file_path)
                    self.update_status(filename, "文件已打开")
                    return file_path
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                        self.text_widget.delete(1.0, tk.END)
                        self.text_widget.insert(1.0, content)
                        self.current_file = file_path
                        self.is_modified = False
                        filename = os.path.basename(file_path)
                        self.update_status(filename, "文件已打开")
                        return file_path
                    except Exception as e:
                        messagebox.showerror("错误", f"文件编码不支持：{str(e)}")
                        return None
                except PermissionError:
                    messagebox.showerror("错误", "文件被占用或没有读取权限")
                    return None
                except Exception as e:
                    messagebox.showerror("错误", f"打开文件失败：{str(e)}")
                    return None
            return None
        except Exception as e:
            messagebox.showerror("错误", f"打开文件失败：{str(e)}")
            return None

    def save_file(self):
        try:
            if self.current_file:
                try:
                    content = self.text_widget.get(1.0, tk.END)
                    with open(self.current_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.is_modified = False
                    filename = os.path.basename(self.current_file)
                    self.update_status(filename, "已保存")
                    return True
                except PermissionError:
                    messagebox.showerror("错误", "文件被占用或没有写入权限")
                    return False
                except Exception as e:
                    messagebox.showerror("错误", f"保存文件失败：{str(e)}")
                    return False
            else:
                return self.save_file_as()
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败：{str(e)}")
            return False

    def save_file_as(self):
        try:
            file_path = filedialog.asksaveasfilename(
                title="另存为",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )

            if file_path:
                try:
                    content = self.text_widget.get(1.0, tk.END)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.current_file = file_path
                    self.is_modified = False
                    filename = os.path.basename(file_path)
                    self.update_status(filename, "已保存")
                    return True
                except PermissionError:
                    messagebox.showerror("错误", "文件被占用或没有写入权限")
                    return False
                except Exception as e:
                    messagebox.showerror("错误", f"另存为失败：{str(e)}")
                    return False
            return False
        except Exception as e:
            messagebox.showerror("错误", f"另存为失败：{str(e)}")
            return False

    def mark_modified(self):
        self.is_modified = True
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.update_status(filename + "*", "已修改")
        else:
            self.update_status("未命名.txt*", "已修改")

    def get_current_file(self):
        return self.current_file

    def is_file_modified(self):
        return self.is_modified
