import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)
    
    def test_tag_not_eq(self):
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="h1")
        self.assertNotEqual(node, node2)
    
    def test_value_not_eq(self):
        node = HTMLNode(value="some text")
        node2 = HTMLNode(value="other text")
        self.assertNotEqual(node, node2)
    
    def test_children_eq(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        children = [child1, child2]
        node = HTMLNode(children=children)
        node2 = HTMLNode(children=children)
        self.assertEqual(node, node2)
    
    def test_props_not_eq(self):
        props1 = {'href': 'https://www.google.com', 'target': '_blank'}
        props2 = {'href': 'https://www.bing.com'}
        node = HTMLNode(props=props1)
        node2 = HTMLNode(props=props2)
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        expected = ' href="https://www.google.com" target="_blank"'
        props = {'href': 'https://www.google.com', 'target': '_blank'}
        node = HTMLNode(props=props)
        res = node.props_to_html()
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()