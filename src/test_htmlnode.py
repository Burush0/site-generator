import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(),expected)

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        expected = "<div><span>child1</span><p>child2</p></div>"
        self.assertEqual(parent_node.to_html(), expected)
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_nested(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        child_node1 = ParentNode("span", [grandchild_node1])
        grandchild_node2 = LeafNode("p", "grandchild2")
        grandchild_node3 = LeafNode("a", "grandchild3", {'href':'https://google.com'})
        child_node2 = ParentNode("div", [grandchild_node2, grandchild_node3])
        child_node3 = ParentNode("h1", [], {'color': 'yellow'})
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        expected = '<div><span><b>grandchild1</b></span><div><p>grandchild2</p><a href="https://google.com">grandchild3</a></div><h1 color="yellow"></h1></div>'
        self.assertEqual(parent_node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()