import os
from collections import OrderedDict
from typing import List, Tuple

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext
from mconv.conversation.line import Line


def make_simple_conversation_yaml() -> Tuple[ConversationContext, str]:
    with open(os.sep.join(['example-datapack', 'data', 'mynamespace', 'functions', 'conv.yaml'])) as file:
        yaml = file.read()

    return make_conv_ctx_simple_conversation_yaml(), yaml


def make_conv_ctx_simple_conversation_yaml() -> ConversationContext:
    return ConversationContext('mynamespace', '', 'conv')


def make_simple_conversation_object() -> Conversation:
    return Conversation(
        make_conv_ctx_simple_conversation_yaml(),
        'Erik',
        [
            Line('Hello!', speak_time=2),
            Line('This is a very long text that requires 3 seconds of reading time', speak_time=3),
            Line('This is the end...', speak_time=2)
        ]
    )


def make_simple_conversation_functions() -> List[Function]:
    def _make_context_from_function_name(function_name: str) -> FunctionContext:
        return FunctionContext(
            namespace='mynamespace',
            path_in_functions_dir='',
            function_name=function_name
        )

    return [
        Function(
            commands=[
                'function mynamespace:conv_1',
                'schedule function mynamespace:conv_2 2s',
                'schedule function mynamespace:conv_3 5s',
            ],
            function_context=_make_context_from_function_name('conv')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(1/3) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                '{"text": "Hello!", "color": "yellow"}'
                ']'
            ],
            function_context=_make_context_from_function_name('conv_1')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(2/3) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                '{"text": "This is a very long text that requires 3 seconds of reading time", "color": "yellow"}'
                ']'
            ],
            function_context=_make_context_from_function_name('conv_2')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(3/3) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                '{"text": "This is the end...", "color": "yellow"}'
                ']'
            ],
            function_context=_make_context_from_function_name('conv_3')
        ),
    ]


def make_conversation_using_json_text_yaml() -> Tuple[ConversationContext, str]:
    with open(os.sep.join(['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text.yaml'])) as file:
        yaml = file.read()

    return make_conv_ctx_using_json_text_yaml(), yaml


def make_conv_ctx_using_json_text_yaml() -> ConversationContext:
    return ConversationContext('mynamespace', 'mydir', 'conv-with-json-text')


def make_conversation_using_json_text_object() -> Conversation:
    return Conversation(
        make_conv_ctx_using_json_text_yaml(),
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
    def _make_context_from_function_name(function_name: str) -> FunctionContext:
        return FunctionContext(
            namespace='mynamespace',
            path_in_functions_dir='mydir',
            function_name=function_name
        )

    return [
        Function(
            commands=['function mynamespace:mydir/conv-with-json-text_1'],
            function_context=_make_context_from_function_name('conv-with-json-text')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(1/1) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "red"}, '
                '{"text": "Hello!", "color": "blue"}'
                ']'
            ],
            function_context=_make_context_from_function_name('conv-with-json-text_1')
        ),
    ]
