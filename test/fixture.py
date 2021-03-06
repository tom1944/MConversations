from collections import OrderedDict
from typing import List, Tuple

from mconv.conversation import Conversation, ConversationContext
from mconv.minecraft.function import Function
from mconv.minecraft.line import Line


def make_simple_conversation_yaml() -> Tuple[ConversationContext, str]:
    with open('example-datapack/data/mynamespace/functions/conv.yaml') as file:
        yaml = file.read()

    return ConversationContext('mynamespace', '', 'conv'), yaml


def make_simple_conversation_object() -> Conversation:
    return Conversation(
        'conv',
        'mynamespace:',
        'Erik',
        [
            Line('Hello!', speak_time=2),
            Line('This is a very long text that requires 3 seconds of reading time', speak_time=3),
            Line('This is the end...', speak_time=2)
        ]
    )


def make_simple_conversation_functions() -> List[Function]:
    return [
            Function(
                name='conv',
                prefix='mynamespace:',
                commands=[
                    'function mynamespace:conv_1',
                    'schedule function mynamespace:conv_2 2s',
                    'schedule function mynamespace:conv_3 5s',
                ]
            ),
            Function(
                name='conv_1',
                prefix='mynamespace:',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(1/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "Hello!", "color": "yellow"}'
                    ']'
                ]
            ),
            Function(
                name='conv_2',
                prefix='mynamespace:',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(2/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "This is a very long text that requires 3 seconds of reading time", "color": "yellow"}'
                    ']'
                ]
            ),
            Function(
                name='conv_3',
                prefix='mynamespace:',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(3/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "This is the end...", "color": "yellow"}'
                    ']'
                ]
            ),
        ]


def make_conversation_using_json_text_yaml() -> Tuple[ConversationContext, str]:
    with open('example-datapack/data/mynamespace/functions/mydir/conv-with-json-text.yaml') as file:
        yaml = file.read()

    return ConversationContext('mynamespace', 'mydir', 'conv-with-json-text'), yaml


def make_conversation_using_json_text_object() -> Conversation:
    return Conversation(
        'conv-with-json-text',
        'mynamespace:mydir/',
        speaker_name=OrderedDict([
            ("text", "Erik"),
            ("color", "red"),
        ]),
        lines=[
            Line(
                OrderedDict([
                    ("text", "Hello!"),
                    ("color", "blue"),
                ]),
                speak_time=2
            ),
        ]
    )


def make_conversation_using_json_text_functions() -> List[Function]:
    return [
            Function(
                name='conv-with-json-text',
                prefix='mynamespace:mydir/',
                commands=[
                    'function mynamespace:mydir/conv-with-json-text_1',
                ]
            ),
            Function(
                name='conv-with-json-text_1',
                prefix='mynamespace:mydir/',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(1/1) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "red"}, '
                    '{"text": "Hello!", "color": "blue"}'
                    ']'
                ]
            ),
        ]
