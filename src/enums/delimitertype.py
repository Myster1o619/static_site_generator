from enum import Enum

class DelimiterType(Enum):
    CODE_DEL = "`"
    BOLD_DEL = "**"
    ITALIC_DEL = "*"
    QUOTE_DEL = "> "
    U_LIST_STAR_DEL = "* "
    U_LIST_DASH_DEL = "- "
    O_LIST_DEL = "1. "