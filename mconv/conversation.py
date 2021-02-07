import copy
from typing import List

from mconv.line import Line


class Conversation:
    def __init__(self, speaker_name: str, lines: List[Line]):
        self.speaker_name = speaker_name
        self.lines = copy.copy(lines)

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return self.speaker_name == other.speaker_name and self.lines == other.lines
