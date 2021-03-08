import copy
from typing import List

from mconv.conversation.conversation_context import ConversationContext
from mconv.minecraft_lang.json_text import JSONText
from mconv.conversation.line import Line


class Conversation:
    def __init__(self, conv_ctx: ConversationContext, speaker_name: JSONText, lines: List[Line]):
        self.ctx = conv_ctx
        self.speaker_name = speaker_name
        self.lines = copy.copy(lines)

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return self.ctx == other.ctx\
            and self.speaker_name == other.speaker_name\
            and self.lines == other.lines
