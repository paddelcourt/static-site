from textnode import TextType, TextNode
from extract import extract_markdown_images, extract_markdown_links
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_in_node = node.text.split(delimiter)
            if len(text_in_node) % 2 == 0:
                raise Exception("invalid markdown, formatted section not closed")
            for i in range(len(text_in_node)):
                if text_in_node[i] == "":
                    continue
                elif i % 2 != 0:
                    new_nodes.append(TextNode(text_in_node[i], text_type))
                else:
                    new_nodes.append(TextNode(text_in_node[i], TextType.TEXT))
                    
        else:
            new_nodes.append(node)
    return new_nodes
            

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
                continue
            
            current_text = node.text
            for image_alt, image_link in images:
                sections = current_text.split(f"![{image_alt}]({image_link})", 1)
                before = sections[0]
                after = sections[1]
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
  
                current_text = after
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))

        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
                continue
            
            current_text = node.text
            for link_alt, link in links:
                sections = current_text.split(f"[{link_alt}]({link})", 1)
                before = sections[0]
                after = sections[1]
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                
                new_nodes.append(TextNode(link_alt, TextType.LINK, link))
  
                current_text = after
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))

        else:
            new_nodes.append(node)
    return new_nodes

                    

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    image = split_nodes_image([node])
    link =  split_nodes_link(image)
    italic = split_nodes_delimiter(link, "_", TextType.ITALIC)
    bold = split_nodes_delimiter(italic,"**", TextType.BOLD)
    code = split_nodes_delimiter(bold,"`", TextType.CODE)
    
    return code


