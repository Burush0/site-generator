import unittest

from generate_site import extract_title


class TestGenerateSite(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Hello

some more md
"""
        result = extract_title(md)
        expected = "Hello"
        self.assertEqual(result, expected)
    
    def test_extract_title_no_header(self):
        md = """
Just some md

and some more md
"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("No h1 header" in str(context.exception))


if __name__ == "__main__":
    unittest.main()