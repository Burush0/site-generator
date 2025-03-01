from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes, TextNode, TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


# 8 helper functions (poggers)
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return block_to_paragraph(block)
        case BlockType.HEADING:
            return block_to_heading(block)
        case BlockType.QUOTE:
            return block_to_quote(block)
        case BlockType.ULIST:
            return block_to_ulist(block)
        case BlockType.OLIST:
            return block_to_olist(block)
        case BlockType.CODE:
            return block_to_code(block)
        case _:
            raise ValueError(f"invalid block type: {block_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_paragraph(block):
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode("p", children)

def block_to_heading(block):
    #lines = block.split("\n")
    #nodes = []
    #for line in lines:
    #    count_hashtags = line.count("#")
    #    heading = f"h{count_hashtags}"
    #    stripped_line = line.lstrip("#")
    #    stripped_line = stripped_line.lstrip(" ")
    #    node = LeafNode(heading, stripped_line)
    #    nodes.append(node)
    # TODO come back to this and figure out a way to return a list of LeafNodes
    count_hashtags = block.count("#")
    heading = f"h{count_hashtags}"
    stripped_block = block.lstrip("#")
    stripped_block = stripped_block.lstrip(" ")
    return LeafNode(heading, stripped_block)
    # return nodes

def block_to_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_olist(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        words = line.split(" ")
        words.pop(0) # remove the "n. " part
        line = " ".join(words)
        grandchildren = text_to_children(line)
        children.append(ParentNode("li", grandchildren))
    return ParentNode("ol", children)

def block_to_ulist(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        words = line.split(" ")
        words.pop(0) # remove the "- " part
        line = " ".join(words)
        grandchildren = text_to_children(line)
        children.append(ParentNode("li", grandchildren))
    return ParentNode("ul", children)

def block_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    block = block.strip("```")
    block = block.lstrip("\n")
    raw = TextNode(block, TextType.TEXT)    
    child = text_node_to_html_node(raw)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

# TODO add images and links as well