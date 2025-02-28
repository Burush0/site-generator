import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
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