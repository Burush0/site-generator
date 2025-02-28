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
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("to_html() method is not implemented")
    
    def props_to_html(self):
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
