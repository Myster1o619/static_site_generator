from enum import Enum

class TextType(Enum):
    TEXT = "normal_text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    QUOTE = "quote"
    LINK = "link"
    IMAGE = "image"
    HEADING_1 = "h1"
    HEADING_2 = "h2"
    HEADING_3 = "h3"
    HEADING_4 = "h4"
    HEADING_5 = "h5"
    HEADING_6 = "h6"
    PARAGRAPH = "paragraph"
    O_LIST = "ordered_list"
    U_LIST = "unordered_list"