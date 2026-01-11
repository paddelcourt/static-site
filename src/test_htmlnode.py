import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(
            "a",
            "link",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none_props_returns_empty_string(self):
        node = HTMLNode("p", "Hello world")
        self.assertEqual(node.props_to_html(),  "")

    def test_constructor_stores_all_fields(self):
        children = [HTMLNode("span", "child")]
        props = {"class": "big"}
        node = HTMLNode("p", "hello", children, props)

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node3 = LeafNode("h1", "Hello, 'world'")
        self.assertEqual(node3.to_html(), "<h1>Hello, 'world'</h1>")

    def test_leaf_error(self):
        node4 = LeafNode("h1", None)
        with self.assertRaises(ValueError):
            node4.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        node = ParentNode("h1", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()