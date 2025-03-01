from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes

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
                children.append(block_to_paragraph(block))
            case BlockType.HEADING:
                children.append(block_to_heading(block))
            case BlockType.QUOTE:
                children.append(block_to_quote(block))
            case BlockType.ULIST:
                children.append(block_to_ulist(block))
            case BlockType.OLIST:
                children.append(block_to_olist(block))
            case BlockType.CODE:
                children.append(block_to_code(block))
            case _:
                raise ValueError(f"invalid block type: {block_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    print(text_nodes)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_paragraph(block):
    block = block.replace("\n", " ")
    children = text_to_children(block)
    parent = ParentNode("p", children)
    return parent

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
    stripped_block = block.lstrip(">")
    stripped_block = stripped_block.lstrip(" ")
    children = text_to_children(stripped_block)
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
    block = block.strip("```")
    child = [LeafNode("code", block)]
    return ParentNode("pre", child)

# TODO add images and links as well

# paragraphs
md = """
This is **bolded** paragraph
text in a p
tag here

# This is a heading 1

## This is a heading 2

### This is a heading 3

> This is a quote with a **bold** and _italic_ words

1. list entry 1
2. list entry 2
3. list entry 3

- bananas
- cherries
- more bananas, _why not_

This is another paragraph with _italic_ text and `code` here

"""
node = markdown_to_html_node(md)
html = node.to_html()
result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
print(html)
print(result)

# code block
md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
node = markdown_to_html_node(md)
html = node.to_html()
result = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
print(html)
print(result)