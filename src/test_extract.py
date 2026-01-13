import unittest

from extract import extract_markdown_images, extract_markdown_links

from website import extract_title


class TestExtract(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_title(self):
        matches = extract_title("""
            # Title One
            ## Subtitle
            This is just text
            """)
        self.assertListEqual(matches,"Title One")

if __name__ == "__main__":
    unittest.main()