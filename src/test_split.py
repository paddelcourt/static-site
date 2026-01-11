import unittest

from textnode import TextNode, TextType

from split import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes



class TestTransformations(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                         [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
])
        
    def test_delim_code_double(self):
        node = TextNode("Use `print()` and `input()` functions", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("print()", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("input()", TextType.CODE),
                TextNode(" functions", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_at_start(self):
        node = TextNode("**bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_at_end(self):
        node = TextNode("Ends with _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Ends with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_entire_text(self):
        node = TextNode("**all bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("all bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_no_delimiter(self):
        node = TextNode("Plain text with no formatting", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Plain text with no formatting", TextType.TEXT),
            ],
            new_nodes,
        )
        
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

    def test_no_image(self):
        node = TextNode("Plain text with no formatting", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Plain text with no formatting", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://www.google.com/maps) and another [second link](https://www.bloomberg.com/europe)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com/maps"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.bloomberg.com/europe"
                ),
            ],
            new_nodes,
        )


    def test_no_link(self):
        node = TextNode("Plain text with no formatting", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Plain text with no formatting", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected_result = [
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
        self.assertListEqual(result, expected_result)




    def test_text_to_textnodes_no_formatting(self):
        text = "This is just plain text with no formatting at all"
        result = text_to_textnodes(text)
        expected_result = [
            TextNode("This is just plain text with no formatting at all", TextType.TEXT)
        ]
        self.assertListEqual(result, expected_result)

    def test_text_to_textnodes_multiple_same_type(self):
        text = "This has **bold** and **more bold** and `code` then `more code`"
        result = text_to_textnodes(text)
        expected_result = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" then ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
        ]
        self.assertListEqual(result, expected_result)

    

if __name__ == "__main__":
    unittest.main()