class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # str, "p", "a", "h1"
        self.value = value # str, e.g. the text inside a paragraph
        self.children = children # list of HTMLNode objects
        self.props = props # dict, attributes of tag
        # e.g. a link (<a> tag) might have {"href": "https://www.google.com"}
        '''
        tag = None -> render as raw text
        value = None -> assumed to have children
        children = None -> assumed to have a value
        props = None -> no attributes
        '''
    
    def __eq__(self, other):
        return (
            self.tag == other.tag 
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("to_html() method is not implemented")
    
    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items())


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value parameter")
        if self.tag is None:
            return self.value
        props = ""
        if self.props != None:
            props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag parameter")
        if self.children is None:
            raise ValueError("ParentNode must have a children parameter")
        props = ""
        if self.props != None:
            props = self.props_to_html()
        children = "".join(list(map(lambda node: node.to_html(), self.children)))
        return f"<{self.tag}{props}>{children}</{self.tag}>"
