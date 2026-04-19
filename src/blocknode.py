from enum import Enum

import re

class BlockType(Enum):
    PARA = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    U_LIST = 5
    O_LIST = 6

def block_to_block_type(block):
    if re.match(r"#{0,6} .*", block):
        return BlockType.HEADING
    if re.match(r"```\n(.|\n)*```", block):
        return BlockType.CODE

    lines = block.split("\n")
    if all(l.startswith(">") for l in lines):
        return BlockType.QUOTE
    if all(l.startswith("-") for l in lines):
        return BlockType.U_LIST

    count = 0
    for l in lines:
        count += 1
        m = re.match(r"(\d+)\. .*", l)
        if m is None or int(m[1]) != count:
            return BlockType.PARA

    return BlockType.O_LIST



def markdown_to_blocks(markdown):
    return list(map(lambda s: s.strip(), markdown.split("\n\n")))
