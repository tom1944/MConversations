from typing import List

from mconv.conversation import Conversation
from mconv.function import Function
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
            Function(
                name=self.conversation.name + '_' + str(index),
                prefix=self.conversation.function_prefix,
                commands=[f'tellraw @a {self._raw_json_text_for_line(line, index)}']
            )
            for index, line in enumerate(self.conversation.lines, start=1)
        ]

    def _raw_json_text_for_line(self, line: Line, index: int) -> str:
        speaker_name = self.conversation.speaker_name
        total_lines = len(self.conversation.lines)

        index_part = '{"text":"(' + str(index) + '/' + str(total_lines) + ') ","bold":true,"color":"gray"}'
        speaker_part = '{"text":"' + speaker_name + ': ","bold":true,"color":"yellow"}'
        text_part = '{"text":"' + line.text + '","color":"yellow"}'

        return '[' + ','.join(['""', index_part, speaker_part, text_part]) + ']'

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
