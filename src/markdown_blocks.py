import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading" # 1-6 #
    CODE = "code" # 3 ` at start and end
    QUOTE = "quote" # every line starts with >
    ULIST = "unordered_list" # starts with - followed by a space
    OLIST = "ordered_list" # 1. 2. etc, numbers must increment

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    heading_matches = []
    code_matches = 0
    quote_matches = []
    ulist_matches = []
    list_matches = []
    for i, line in enumerate(lines):
        heading_match = re.findall(r"^#{1,6}\s.+$", line)
        code_matches = 0
        if lines[0].startswith("```"):
            code_matches += 1
        if lines[-1].endswith("```"):
            code_matches += 1
        quote_match = re.findall(r"^>.+$", line)
        ulist_match = re.findall(r"^-\s.+$", line)
        list_match = re.findall(rf"^{i+1}\.\s", line)
        if heading_match:
            heading_matches.append(heading_match)
        if quote_match:
            quote_matches.append(quote_match)
        if ulist_match:
            ulist_matches.append(ulist_match)
        if list_match:
            list_matches.append(list_match)
    if len(lines) == len(heading_matches):
        return BlockType.HEADING
    if code_matches == 2:
        return BlockType.CODE
    if len(lines) == len(quote_matches):
        return BlockType.QUOTE
    if len(lines) == len(ulist_matches):
        return BlockType.ULIST
    if len(lines) == len(list_matches):
        return BlockType.OLIST
    return BlockType.PARAGRAPH
