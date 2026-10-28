import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
                    blocks,
                    [
                        "This is **bolded** paragraph",
                        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                        "- This is a list\n- with items",
                    ],
                )

class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Heading without space"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        valid_code = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(valid_code), BlockType.CODE)

        invalid_code = "```print('hello')```"
        self.assertEqual(block_to_block_type(invalid_code), BlockType.PARAGRAPH)

        unclosed_code = "```\nx = 10"
        self.assertEqual(block_to_block_type(unclosed_code), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">No space quote"), BlockType.QUOTE)

        multiline_quote = "> First line\n> Second line\n> Third line"
        self.assertEqual(block_to_block_type(multiline_quote), BlockType.QUOTE)

        invalid_quote = "> First line\nSecond line without quote\n> Third line"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_unordered_list_blocks(self):
        self.assertEqual(block_to_block_type("- Item single"), BlockType.UNORDERED_LIST)

        valid_ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(valid_ul), BlockType.UNORDERED_LIST)

        invalid_ul = "- Item 1\n* Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(invalid_ul), BlockType.PARAGRAPH)

        invalid_ul_format = "-Item without space"
        self.assertEqual(block_to_block_type(invalid_ul_format), BlockType.PARAGRAPH)

    def test_ordered_list_blocks(self):
        valid_ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(valid_ol), BlockType.ORDERED_LIST)

        invalid_start = "2. Two\n3. Three"
        self.assertEqual(block_to_block_type(invalid_start), BlockType.PARAGRAPH)

        invalid_sequence = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(invalid_sequence), BlockType.PARAGRAPH)

        invalid_format = "1 First\n2 Second"
        self.assertEqual(block_to_block_type(invalid_format), BlockType.PARAGRAPH)

    def test_paragraph_blocks(self):
        text = "This is just a normal paragraph with multiple words."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

        multiline_text = "This is a paragraph\nthat spans across multiple\nlines."
        self.assertEqual(block_to_block_type(multiline_text), BlockType.PARAGRAPH)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "#   Tolkien Fan Club   \nSome paragraph"
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_extract_title_raises_exception(self):
        md = "## Only h2 header\nNo h1 here"
        with self.assertRaises(Exception):
            extract_title(md)

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
