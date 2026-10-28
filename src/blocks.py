from enum import Enum

from htmlnode import ParentNode
from inline import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType (Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []

    raw_blocks = markdown.strip().split("\n\n")
    blocks = []

    for block in raw_blocks:
        lines = block.splitlines()
        cleaned_lines = []

        for line in lines:
            clean = line.strip()
            if clean:
                cleaned_lines.append(clean)

        cleaned_block = "\n".join(cleaned_lines)

        if cleaned_block:
            blocks.append(cleaned_block)

    return blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if lines and all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    text = block[3:-3]
    text = text.removeprefix("\n")

    text_node = TextNode(text, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [code_child])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())
    content = " ".join(cleaned_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()
    items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def olist_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()
    items = []
    for line in lines:
        text = line[line.find(". ") + 2 :]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)

    raise ValueError("Invalid block type")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
