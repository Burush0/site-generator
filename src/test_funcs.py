import unittest

from textnode import TextNode, TextType
from funcs import *


class TestFuncs(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {'href': 'https://boot.dev'})
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "../boots.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': '../boots.png', 'alt': 'This is an image'})

    def test_other_type(self):
        node = TextNode("some text", "not an enum")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Not a valid text type!")
    
    def test_delimiter(self):
        node = TextNode("This is `code`", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [TextNode("This is ", TextType.TEXT), TextNode("code", TextType.CODE)]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_multiple_delimiter_pair(self):
        node = TextNode("This is `code` and `some more code`", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("some more code", TextType.CODE)]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_delimiter_sequence(self):
        node = TextNode("This is `code` and **some bold text**", TextType.TEXT)
        code_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        split_nodes = split_nodes_delimiter(code_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("some bold text", TextType.BOLD)]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_delimiter_at_start(self):
        node = TextNode("**Bold text** is cool to have at start", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold text", TextType.BOLD), 
            TextNode(" is cool to have at start", TextType.TEXT)]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_adjacent_delimiters(self):
        node = TextNode("This is _italic text_**bold text**", TextType.TEXT)
        italic_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        split_nodes = split_nodes_delimiter(italic_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT), 
            TextNode("italic text", TextType.ITALIC),
            TextNode("bold text", TextType.BOLD)]
        self.assertEqual(split_nodes, expected_nodes)
    
    def test_unmatched_delimiter(self):
        node = TextNode("This is **bold text that stayed bold", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Unmatched delimiter: **")
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This text with ![image1](https://i.imgur.com/test123.png) and ![image2](https://i.imgur.com/test456.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/test123.png"), ("image2", "https://i.imgur.com/test456.png")], matches)

    def test_extract_only_image(self):
        matches = extract_markdown_images(
            "![image](https://imgurl) and a [link](https://linkurl)"
        )
        self.assertListEqual([("image", "https://imgurl")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://linkurl)"
        )
        self.assertListEqual([("link", "https://linkurl")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[link](https://link1) and [link](https://link2)"
        )
        self.assertListEqual([("link", "https://link1"), ("link", "https://link2")], matches)
    
    def test_extract_only_link(self):
        matches = extract_markdown_links(
            "![image](https://imgurl) and a [link](https://linkurl)"
        )
        self.assertListEqual([("link", "https://linkurl")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
           new_nodes,
        )

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![alt](url) and more text",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" and more text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        node = TextNode(
            "![alt](url) starts here",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" starts here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode(
            "Ends with ![alt](url)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Ends with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)
    
    def test_no_images(self):
        node = TextNode(
            "No images here, just text.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("No images here, just text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )
    
    def test_single_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and more text",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and more text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode(
            "[start](https://start.com) of the text",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "https://start.com"),
            TextNode(" of the text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode(
            "The text ends with a [link](https://end.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("The text ends with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://end.com"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode(
            "This has no links, only text.",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This has no links, only text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(input)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)
    
    def test_empty_string(self):
        input = ""
        result = text_to_textnodes(input)
        expected = []
        self.assertEqual(result, expected)

    def test_only_text(self):
        input = "This is just plain text."
        result = text_to_textnodes(input)
        expected = [
            TextNode("This is just plain text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_only_bold(self):
        input = "**bold text**"
        result = text_to_textnodes(input)
        expected = [
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_only_italic(self):
        input = "_italic text_"
        result = text_to_textnodes(input)
        expected = [
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_only_code(self):
        input = "`code block`"
        result = text_to_textnodes(input)
        expected = [
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_only_image(self):
        input = "![alt text](https://example.com/image.png)"
        result = text_to_textnodes(input)
        expected = [
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(result, expected)

    def test_only_link(self):
        input = "[link text](https://example.com)"
        result = text_to_textnodes(input)
        expected = [
            TextNode("link text", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)
    
    def test_mixed_formats_without_spaces(self):
        input = "**bold**_italic_`code`![image](https://example.com/image.png)[link](https://example.com)"
        result = text_to_textnodes(input)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()