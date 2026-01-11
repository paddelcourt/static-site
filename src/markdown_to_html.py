
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode
from convert_node import text_node_to_html_node
from split import text_to_textnodes
from textnode import TextNode, TextType
import re


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for i in text_nodes:
        html_node = text_node_to_html_node(i)
        children.append(html_node)
    return children



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    final_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            normalized = block.replace("\n", " ")
            normalized = re.sub(r"\s+", " ", normalized).strip()
            children = text_to_children(normalized)
            html_node = ParentNode("p", children)
        elif block_type == "heading":
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1
            heading_type = "h" + str(level)
            content = block[level:].lstrip()  
            children = text_to_children(content)
            html_node = ParentNode(heading_type, children)
        elif block_type == "quote":
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                if line.startswith("> "):
                    line = line[2:]
                cleaned_lines.append(line)
            cleaned_text = "\n".join(cleaned_lines)
            children = text_to_children(cleaned_text)
            html_node = ParentNode("blockquote", children)
        elif block_type == "unordered_list":
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                if line.startswith("- "):
                    line = line[2:]
                cleaned_line_node = text_to_children(line)
                li_nodes.append(ParentNode("li", cleaned_line_node))
            html_node = ParentNode("ul", li_nodes)
        elif block_type == "ordered_list":
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                line = re.sub(r"^\d+\.\s*", "", line)
                cleaned_line_node = text_to_children(line)
                li_nodes.append(ParentNode("li", cleaned_line_node))
            html_node = ParentNode("ol", li_nodes)
        elif block_type == "code":
            lines = block.split("\n") 
            inner_lines = lines[1:-1]
            new_block = "\n".join(inner_lines)
            text_node = TextNode(new_block, TextType.TEXT)
            code_child = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [code_child])
            html_node = ParentNode("pre", [code_node])
        else:
            raise Exception(f"Unknown block type: {block_type}")
        print(final_children)
        final_children.append(html_node)

    return ParentNode("div", final_children)
        


        