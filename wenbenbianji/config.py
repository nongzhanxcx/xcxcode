"""
配置文件：存储文本编辑器的常量配置
包含窗口尺寸、默认字体、颜色值、快捷键映射等
"""

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "自定义文本编辑器"
VERSION = "1.0.0"

DEFAULT_FONT_FAMILY = "Consolas"
DEFAULT_FONT_SIZE = 12
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 24

BACKGROUND_COLORS = {
    "white": "#FFFFFF",
    "light_gray": "#F0F0F0",
    "light_blue": "#E6F3FF"
}

FONT_SIZES = [12, 14, 16]

SHORTCUT_KEYS = {
    "new": "<Control-n>",
    "open": "<Control-o>",
    "save": "<Control-s>",
    "copy": "<Control-c>",
    "cut": "<Control-x>",
    "paste": "<Control-v>",
    "find": "<Control-f>",
    "select_all": "<Control-a>"
}

PYTHON_KEYWORDS = [
    "def", "class", "if", "else", "elif", "for", "while", "try", "except",
    "finally", "with", "import", "from", "as", "return", "yield", "raise",
    "pass", "break", "continue", "and", "or", "not", "in", "is", "lambda",
    "True", "False", "None", "print", "input", "len", "range", "list",
    "dict", "set", "tuple", "str", "int", "float", "bool"
]

C_KEYWORDS = [
    "int", "float", "double", "char", "void", "if", "else", "elif", "for",
    "while", "do", "switch", "case", "break", "continue", "return", "goto",
    "sizeof", "typedef", "struct", "union", "enum", "const", "static",
    "extern", "volatile", "auto", "register", "signed", "unsigned", "include",
    "define", "undef", "ifdef", "ifndef", "endif", "main", "printf", "scanf"
]

MAX_RECENT_FILES = 3
