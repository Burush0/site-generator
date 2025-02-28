from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag parameter")
        if self.children == None:
            raise ValueError("ParentNode must have a children parameter")
        props = ""
        if self.props != None:
            props = self.props_to_html()
        children = "".join(list(map(lambda node: node.to_html(), self.children)))
        return f"<{self.tag}{props}>{children}</{self.tag}>"
