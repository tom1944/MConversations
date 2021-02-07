import copy
from typing import List

from mconv.line import Line


class Conversation:
    def __init__(self, function_prefix: str, speaker_name: str, lines: List[Line]):
        self.function_prefix = function_prefix
        self.speaker_name = speaker_name
        self.lines = copy.copy(lines)

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return self.function_prefix == other.function_prefix\
            and self.speaker_name == other.speaker_name\
            and self.lines == other.lines
