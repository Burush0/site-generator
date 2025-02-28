import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is a heading")
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")

    def test_leaf_to_html_props(self):
        props = {'href': 'https://www.google.com', 'target': '_blank'}
        node = LeafNode("a", "This is a link", props)
        expected = '<a href="https://www.google.com" target="_blank">This is a link</a>'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()