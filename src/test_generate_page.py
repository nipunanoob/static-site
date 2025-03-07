import unittest

from page_generate import  extract_title

class TestPageGenerate(unittest.TestCase):
    def test_valid_extract_title(self):
        markdown1 = "# hello   \n##Jerry  "
        markdown2 = "# hello"
        self.assertEqual(extract_title(markdown1), "hello")
        self.assertEqual(extract_title(markdown2), "hello")

    def test_invalid_extract_title(self):
        markdown = "## title"
        with self.assertRaisesRegex(ValueError, "Markdown string does not start with h1 header"):
            extract_title(markdown)