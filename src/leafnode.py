from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value parameter")
        if self.tag == None:
            return self.value
        props = ""
        if self.props != None:
            props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"