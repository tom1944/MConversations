from collections import OrderedDict
from typing import List

from mconv.conversation import Conversation
from mconv.function import Function
from mconv.line import Line


def make_simple_conversation_yaml() -> str:
    return '\n'.join([
        'function-prefix: mynamespace:path/to/dir/',
        'speaker-name: Erik',
        'default-speak-time-sec: 2',
        'conversation:',
        '  - say: Hello!',
        '  - say: This is a very long text that requires 3 seconds of reading time',
        '    speak-time-sec: 3',
        '  - say: This is the end...',
    ])


def make_simple_conversation_object() -> Conversation:
    return Conversation(
        'conv1',
        'mynamespace:path/to/dir/',
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
                name='conv1',
                prefix='mynamespace:path/to/dir/',
                commands=[
                    'function mynamespace:path/to/dir/conv1_1',
                    'schedule function mynamespace:path/to/dir/conv1_2 2s',
                    'schedule function mynamespace:path/to/dir/conv1_3 5s',
                ]
            ),
            Function(
                name='conv1_1',
                prefix='mynamespace:path/to/dir/',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(1/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "Hello!", "color": "yellow"}'
                    ']'
                ]
            ),
            Function(
                name='conv1_2',
                prefix='mynamespace:path/to/dir/',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(2/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "This is a very long text that requires 3 seconds of reading time", "color": "yellow"}'
                    ']'
                ]
            ),
            Function(
                name='conv1_3',
                prefix='mynamespace:path/to/dir/',
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(3/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "This is the end...", "color": "yellow"}'
                    ']'
                ]
            ),
        ]


def make_conversation_using_json_text_yaml() -> str:
    return '\n'.join([
        'function-prefix: mynamespace:mydir/',
        'speaker-name: {"text": "Erik", "color": "red"}',
        'default-speak-time-sec: 2',
        'conversation:',
        '  - say: {"text": "Hello!", "color": "blue"}',
    ])


def make_conversation_using_json_text_object() -> Conversation:
    return Conversation(
        'conv2',
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
                name='conv2',
                prefix='mynamespace:mydir/',
                commands=[
                    'function mynamespace:mydir/conv2_1',
                ]
            ),
            Function(
                name='conv2_1',
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
