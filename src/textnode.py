from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold" # **
    ITALIC = "italic" # _
    CODE = "code" # `
    LINK = "link" # [anchor](url)
    IMAGE = "image" # ![alt](url)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading" # 1-6 #
    CODE = "code" # 3 ` at start and end
    QUOTE = "quote" # every line starts with >
    ULIST = "unordered_list" # starts with - followed by a space
    LIST = "ordered_list" # 1. 2. etc, numbers must increment

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
