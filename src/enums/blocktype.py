from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    # HEADING = "# "
    HEADING_1 = "# "
    HEADING_2 = "## "
    HEADING_3 = "### "
    HEADING_4 = "#### "
    HEADING_5 = "##### "
    HEADING_6 = "###### "
    CODE = "```"
    QUOTE = ">"
    UL_STAR = "* "
    UL_DASH = "- "
    OL = "ordered_list"
