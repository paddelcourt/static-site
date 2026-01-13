from enum import Enum
import re


class BlockType(Enum):
        PARAGRAPH = "paragraph"
        HEADING = "heading"
        QUOTE = "quote"
        CODE = "code"
        UNORDERED_LIST = "unordered_list"
        ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
     
    new_blocks = []
    for i in blocks:
        block_strip = i.strip()
        if block_strip:
            new_blocks.append(block_strip)
    return new_blocks


def block_to_block_type(block):
    if re.match(r"^(#{1,6})\s+.+$", block):
         return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
         return BlockType.CODE
    
    new_block = block.split("\n")
    if all(i.startswith(">") for i in new_block):
        return BlockType.QUOTE
    elif all(i.startswith("- ") for i in new_block):
        return BlockType.UNORDERED_LIST
    elif new_block[0][0] == "1":
         counter = 1
         for i in new_block:
              if re.match("/[0-9]+\./", i) and i[0] == counter:
                   counter = counter + 1
              else:
                   break
         return BlockType.ORDERED_LIST
    else:
         return BlockType.PARAGRAPH
         
         
     
