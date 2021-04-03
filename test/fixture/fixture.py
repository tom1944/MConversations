import os
from collections import OrderedDict
from typing import List, Tuple, NamedTuple

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext
from mconv.conversation.line import Line


class MConvTestFixture(NamedTuple):
    file_path: str
    yaml: str

    conv_ctx: ConversationContext
    conversation: Conversation

    functions: List[Function]


def make_conv_fixtures() -> List[MConvTestFixture]:
    return [
        make_simple_conv_fixture(),
        make_conv_with_json_text_fixture(),
    ]


def make_simple_conv_fixture() -> MConvTestFixture:
    file_path = os.sep.join(['example-datapack', 'data', 'mynamespace', 'functions', 'conv.yaml'])

    with open(file_path) as file:
        yaml = file.read()

    conv_ctx = ConversationContext('mynamespace', '', 'conv')

    conversation = Conversation(
        conv_ctx,
        'Erik',
        [
            Line('Hello!', speak_time=2),
            Line('This is a very long text that requires 3 seconds of reading time', speak_time=3),
            Line('This is the end...', speak_time=2)
        ]
    )

    fcc = _FunctionContextCreator('mynamespace', '')

    functions = [
        Function(
            commands=[
                'function mynamespace:conv_1',
                'schedule function mynamespace:conv_2 2s',
                'schedule function mynamespace:conv_3 5s',
            ],
            function_context=fcc.make_function_context('conv')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(1/3) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                '{"text": "Hello!", "color": "yellow"}'
                ']'
            ],
            function_context=fcc.make_function_context('conv_1')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(2/3) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                '{"text": "This is a very long text that requires 3 seconds of reading time", "color": "yellow"}'
                ']'
            ],
            function_context=fcc.make_function_context('conv_2')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(3/3) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                '{"text": "This is the end...", "color": "yellow"}'
                ']'
            ],
            function_context=fcc.make_function_context('conv_3')
        ),
    ]

    return MConvTestFixture(file_path, yaml, conv_ctx, conversation, functions)


def make_simple_conversation_yaml() -> Tuple[ConversationContext, str]:
    simple_conv_fixture = make_simple_conv_fixture()
    return simple_conv_fixture.conv_ctx, simple_conv_fixture.yaml


def make_conv_ctx_simple_conversation_yaml() -> ConversationContext:
    return make_simple_conv_fixture().conv_ctx


def make_simple_conversation_object() -> Conversation:
    return make_simple_conv_fixture().conversation


def make_simple_conversation_functions() -> List[Function]:
    return make_simple_conv_fixture().functions


def make_conv_with_json_text_fixture() -> MConvTestFixture:
    file_path = os.sep.join(['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text.yaml'])

    with open(file_path) as file:
        yaml = file.read()

    conv_ctx = ConversationContext('mynamespace', 'mydir', 'conv-with-json-text')

    conversation = Conversation(
        conv_ctx,
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

    fcc = _FunctionContextCreator('mynamespace', 'mydir')

    functions = [
        Function(
            commands=['function mynamespace:mydir/conv-with-json-text_1'],
            function_context=fcc.make_function_context('conv-with-json-text')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(1/1) ", "color": "gray", "bold": true}, '
                '{"text": "Erik: ", "color": "red"}, '
                '{"text": "Hello!", "color": "blue"}'
                ']'
            ],
            function_context=fcc.make_function_context('conv-with-json-text_1')
        ),
    ]

    return MConvTestFixture(file_path, yaml, conv_ctx, conversation, functions)


def make_conversation_using_json_text_yaml() -> Tuple[ConversationContext, str]:
    conversation_using_json_text = make_conv_with_json_text_fixture()
    return conversation_using_json_text.conv_ctx, conversation_using_json_text.yaml


def make_conv_ctx_using_json_text_yaml() -> ConversationContext:
    return make_conv_with_json_text_fixture().conv_ctx


def make_conversation_using_json_text_object() -> Conversation:
    return make_conv_with_json_text_fixture().conversation


def make_conversation_using_json_text_functions() -> List[Function]:
    return make_conv_with_json_text_fixture().functions


class _FunctionContextCreator:
    def __init__(self, namespace: str, path_in_functions_dir: str):
        self.namespace = namespace
        self.path_in_functions_dir = path_in_functions_dir

    def make_function_context(self, function_name: str) -> FunctionContext:
        return FunctionContext(
            self.namespace,
            self.path_in_functions_dir,
            function_name
        )
