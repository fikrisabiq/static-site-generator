import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_error(self):
        htmlnode = HTMLNode()
        with self.assertRaises(NotImplementedError):
            htmlnode.to_html()

    def test_props_to_html(self):
        props = {"href": "https://www.google.com","target": "_blank"}
        htmlnode = HTMLNode(props = props)
        res = htmlnode.props_to_html()
        self.assertEqual(res,  ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_None(self):
        htmlnode = HTMLNode()
        res = htmlnode.props_to_html()
        self.assertEqual(res, "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", "", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_props(self):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
            self.assertEqual(
                parent_node.to_html(),
                '<div class="container" id="main"><span>child</span></div>',
            )

if __name__ == "__main__":
    unittest.main()
