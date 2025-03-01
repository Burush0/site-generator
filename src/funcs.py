import re
from textnode import TextNode, TextType, BlockType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception("Not a valid text type!")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)
        
        # delimiter has to have a start and an end
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter: {delimiter}")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 1:
                current_type = text_type
            else:
                current_type = TextType.TEXT
            new_nodes.append(TextNode(parts[i], current_type))
        
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) 
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extract_markdown_images(remaining_text)
        if not matches:
                new_nodes.append(old_node)
                continue
        
        for match in matches:
            image_alt, image_link = match[0], match[1]
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extract_markdown_links(remaining_text)

        if not matches:
            new_nodes.append(old_node)
            continue

        for match in matches:
            hyperlink, url = match[0], match[1]
            sections = remaining_text.split(f"[{hyperlink}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
            new_nodes.append(TextNode(hyperlink, TextType.LINK, url))

            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
            matches = extract_markdown_links(remaining_text)
    
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [node], "**", TextType.BOLD
                    ), "_", TextType.ITALIC
                ), "`", TextType.CODE)
            )
    )

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
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
        return BlockType.LIST
    return BlockType.PARAGRAPH


