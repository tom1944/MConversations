import json
from collections import OrderedDict
from typing import List

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext
from mconv.minecraft_lang.json_text import JSONText
from mconv.conversation.line import Line


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
            LineFunctionCreator(line, index, self.conversation).create_line()
            for index, line in enumerate(self.conversation.lines, start=1)
        ]

    def _make_conversation_function(self, line_functions: List[Function]) -> Function:
        return Function(
            self._make_commands_from_line_functions(line_functions),
            _conv_ctx_to_func_ctx(
                self.conversation.ctx,
                self.conversation.ctx.name
            )
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
        return f'function {func.get_qualified_function_name()}'
    else:
        return f'schedule function {func.get_qualified_function_name()} {time}s'


class LineFunctionCreator:
    def __init__(self, line: Line, index: int, conversation: Conversation):
        self.line = line
        self.index = index
        self.conversation = conversation
        self.conv_ctx = conversation.ctx

    def create_line(self) -> Function:
        function_name = self.conv_ctx.name + '_' + str(self.index)

        return Function(
            commands=['tellraw @a ' + self._raw_json_text_for_line()],
            function_context=_conv_ctx_to_func_ctx(
                self.conv_ctx,
                function_name
            )
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
        total_lines = len(self.conversation.lines)
        return OrderedDict([
            ("text", "(" + str(self.index) + "/" + str(total_lines) + ")"),
            ("color", "gray"),
            ("bold", True),
        ])

    def make_json_text_for_speaker_part(self) -> JSONText:
        speaker_name = self.conversation.speaker_name

        if isinstance(speaker_name, str):
            return OrderedDict([
                ("text", speaker_name),
                ("color", "yellow"),
                ("bold", True),
            ])
        else:
            return speaker_name

    def _make_json_text_for_text_part(self) -> JSONText:
        if isinstance(self.line.text, str):
            return OrderedDict([
                ("text", self.line.text),
                ("color", "yellow"),
            ])
        else:
            return self.line.text


def _conv_ctx_to_func_ctx(conv_ctx: ConversationContext, func_name: str) -> FunctionContext:
    return FunctionContext(
        conv_ctx.namespace,
        conv_ctx.path_in_functions_dir,
        func_name
    )
