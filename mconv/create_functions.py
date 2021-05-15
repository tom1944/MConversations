import json
from collections import OrderedDict
from typing import List

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.conversation.line import TextLine, FunctionLine
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext
from mconv.minecraft_lang.json_text import JSONText
from mconv.talk_lock_functions import make_command_that_executes_function_if_talk_lock_is_free, \
    LOCK_TALK_LOCK_FUNCTION, GLOBAL_NAMESPACE, FREE_TALK_LOCK_FUNCTION


def create_functions(conversation: Conversation) -> List[Function]:
    return ConversationFunctionsCreator(conversation).create_functions()


class ConversationFunctionsCreator:
    def __init__(self, conversation: Conversation):
        self.conversation = conversation

    def create_functions(self) -> List[Function]:
        line_functions = self._make_line_functions()
        conv_function = self._make_conversation_function(line_functions)
        guard_function = self._make_guard_function(conv_function)
        return [guard_function, conv_function] + line_functions

    def _make_line_functions(self) -> List[Function]:
        text_lines = [line for line in self.conversation.lines if isinstance(line, TextLine)]
        text_line_count = len(text_lines)

        return [
            TextLineFunctionCreator(line, index, text_line_count, self.conversation).create_line_function()
            for index, line in enumerate(text_lines, start=1)
        ]

    def _make_conversation_function(self, line_functions: List[Function]) -> Function:
        return Function(
            self._make_commands_for_line_functions(line_functions),
            _conv_ctx_to_func_ctx(
                self.conversation.ctx,
                self.conversation.ctx.name + '_no_lock'
            )
        )

    def _make_commands_for_line_functions(self, line_functions: List[Function]) -> List[str]:
        commands = []
        line_func_it = iter(line_functions)
        time = 0

        commands.append(
            _make_schedule_command(f'{GLOBAL_NAMESPACE}:{LOCK_TALK_LOCK_FUNCTION}', time)
        )

        for line in self.conversation.lines:
            if isinstance(line, TextLine):
                func = next(line_func_it)
                commands.append(
                    _make_schedule_command(func.get_qualified_function_name(), time)
                )
                speak_time = line.speak_time
                time += speak_time
            elif isinstance(line, FunctionLine):
                commands.append(
                    _make_schedule_command(line.qualified_function_name, time)
                )
            else:
                raise Exception("Unknown Line subclass")

        time -= speak_time

        commands.append(
            _make_schedule_command(f'{GLOBAL_NAMESPACE}:{FREE_TALK_LOCK_FUNCTION}', time)
        )

        return commands

    def _make_guard_function(self, conv_function: Function) -> Function:
        context = self.conversation.ctx
        conv_function_name = conv_function.context.as_qualified_function_name()

        return Function(
            [
                make_command_that_executes_function_if_talk_lock_is_free(conv_function_name)
            ],
            _conv_ctx_to_func_ctx(context, context.name)
        )


def _make_schedule_command(func_name: str, time: int) -> str:
    if time == 0:
        return f'function {func_name}'
    else:
        return f'schedule function {func_name} {time}s'


class TextLineFunctionCreator:
    def __init__(self, text_line: TextLine, index: int, total_text_lines: int, conversation: Conversation):
        self.text_line = text_line
        self.index = index
        self.total_text_lines = total_text_lines
        self.conversation = conversation
        self.conv_ctx = conversation.ctx

    def create_line_function(self) -> Function:
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
        speaker_part = self._make_json_text_for_speaker_part()
        speaker_part['text'] += ": "
        text_part = self._make_json_text_for_text_part()

        json_text_as_json_object = ["", index_part, speaker_part, text_part]

        return json.dumps(json_text_as_json_object)

    def _make_json_text_for_index_part(self) -> JSONText:
        return OrderedDict([
            ("text", "(" + str(self.index) + "/" + str(self.total_text_lines) + ")"),
            ("color", "gray"),
            ("bold", True),
        ])

    def _make_json_text_for_speaker_part(self) -> JSONText:
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
        if isinstance(self.text_line.text, str):
            return OrderedDict([
                ("text", self.text_line.text),
                ("color", "yellow"),
            ])
        else:
            return self.text_line.text


def _conv_ctx_to_func_ctx(conv_ctx: ConversationContext, func_name: str) -> FunctionContext:
    return FunctionContext(
        conv_ctx.namespace,
        conv_ctx.path_in_functions_dir,
        func_name
    )
