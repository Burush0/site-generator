import unittest

from textnode import TextNode, TextType
from funcs import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is  a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_url_eq(self):
        node = TextNode("This is a url node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a url node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("This is an image node", TextType.IMAGE, "../maxresdefault.png")
        node2 = TextNode("This is an image node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()