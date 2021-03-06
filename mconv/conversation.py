import copy
from typing import List

from mconv.minecraft.json_text import JSONText
from mconv.minecraft.line import Line


class Conversation:
    def __init__(self, name: str, function_prefix: str, speaker_name: JSONText, lines: List[Line]):
        self.name = name
        self.function_prefix = function_prefix
        self.speaker_name = speaker_name
        self.lines = copy.copy(lines)

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return self.name == other.name\
            and self.function_prefix == other.function_prefix\
            and self.speaker_name == other.speaker_name\
            and self.lines == other.lines
