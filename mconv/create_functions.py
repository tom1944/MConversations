import json
from collections import OrderedDict
from typing import List

from mconv.conversation import Conversation
from mconv.function import Function
from mconv.json_text import JSONText
from mconv.line import Line


def create_functions(conversation: Conversation) -> List[Function]:
    return FunctionCreator(conversation).create_functions()


class FunctionCreator:
    def __init__(self, conversation: Conversation):
        self.conversation = conversation

    def create_functions(self) -> List[Function]:
        line_functions = self._make_line_functions()
        conv_function = self._make_conversation_function(line_functions)
        return [conv_function] + line_functions

    def _make_line_functions(self) -> List[Function]:
        return [
            LineFunctionCreator(line, index, conversation_context=self.conversation).create_line()
            for index, line in enumerate(self.conversation.lines, start=1)
        ]

    def _make_conversation_function(self, line_functions: List[Function]) -> Function:
        return Function(
            name=self.conversation.name,
            prefix=self.conversation.function_prefix,
            commands=self._make_commands_from_line_functions(line_functions)
        )

    def _make_commands_from_line_functions(self, line_functions: List[Function]) -> List[str]:
        commands = []
        time = 0

        for line, func in zip(self.conversation.lines, line_functions):
            commands.append(
                _make_schedule_command(func, time)
            )
            time += line.speak_time

        return commands


def _make_schedule_command(func: Function, time: int) -> str:
    if time == 0:
        return f'function {func.get_identifier()}'
    else:
        return f'schedule function {func.get_identifier()} {time}s'


class LineFunctionCreator:
    def __init__(self, line: Line, index: int, conversation_context: Conversation):
        self.line = line
        self.index = index
        self.conversation_context = conversation_context

    def create_line(self) -> Function:
        return Function(
            name=self.conversation_context.name + '_' + str(self.index),
            prefix=self.conversation_context.function_prefix,
            commands=['tellraw @a ' + self._raw_json_text_for_line()]
        )

    def _raw_json_text_for_line(self) -> str:
        index_part = self._make_json_text_for_index_part()
        index_part['text'] += " "
        speaker_part = self.make_json_text_for_speaker_part()
        speaker_part['text'] += ": "
        text_part = self._make_json_text_for_text_part()

        json_text_as_json_object = ["", index_part, speaker_part, text_part]

        return json.dumps(json_text_as_json_object)

    def _make_json_text_for_index_part(self) -> JSONText:
        total_lines = len(self.conversation_context.lines)
        return OrderedDict([
            ("text", "(" + str(self.index) + "/" + str(total_lines) + ")"),
            ("color", "gray"),
            ("bold", True),
        ])

    def make_json_text_for_speaker_part(self) -> JSONText:
        speaker_name = self.conversation_context.speaker_name
        speaker_part = OrderedDict([
            ("text", speaker_name),
            ("color", "yellow"),
            ("bold", True),
        ])
        return speaker_part

    def _make_json_text_for_text_part(self) -> JSONText:
        return OrderedDict([
            ("text", self.line.text),
            ("color", "yellow"),
        ])
