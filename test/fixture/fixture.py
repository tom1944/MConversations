import os
from collections import OrderedDict
from typing import List, NamedTuple

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext
from mconv.conversation.line import TextLine, FunctionLine


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
        make_conv_with_function_fixture(),
    ]


def make_list_of_generated_function_files() -> List[str]:
    files = [
        ['example-datapack', 'data', 'zzz_mconv', 'functions', 'init.mcfunction'],
        ['example-datapack', 'data', 'zzz_mconv', 'functions', 'lock_talk_lock.mcfunction'],
        ['example-datapack', 'data', 'zzz_mconv', 'functions', 'free_talk_lock.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'conv.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'conv_1.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'conv_2.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'conv_3.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text_1.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'subdir', 'conv-reward-function.mcfunction'],
        ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'subdir', 'conv-reward-function_1.mcfunction']
    ]

    return [os.sep.join(path) for path in files]


def make_simple_conv_fixture() -> MConvTestFixture:
    file_path = os.sep.join(['example-datapack', 'data', 'mynamespace', 'functions', 'conv.yaml'])

    with open(file_path) as file:
        yaml = file.read()

    conv_ctx = ConversationContext('mynamespace', '', 'conv')

    conversation = Conversation(
        conv_ctx,
        'Erik',
        [
            TextLine('Hello!', speak_time=2),
            TextLine('This is a very long text that requires 3 seconds of reading time', speak_time=3),
            TextLine('This is the end...', speak_time=2)
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


def make_conv_with_json_text_fixture() -> MConvTestFixture:
    file_path = os.sep.join(
        ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text.yaml']
    )

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
            TextLine(
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


def make_conv_with_function_fixture() -> MConvTestFixture:
    file_path = os.sep.join(
        ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'subdir', 'conv-reward-function.yaml']
    )

    with open(file_path) as file:
        yaml = file.read()

    conv_ctx = ConversationContext('mynamespace', f'mydir{os.sep}subdir', 'conv-reward-function')

    conversation = Conversation(
        conv_ctx,
        speaker_name='John',
        lines=[
            TextLine(
                text='You earned a reward!',
                speak_time=2
            ),
            FunctionLine(
                qualified_function_name='mynamespace:rewarding-function'
            )
        ]
    )

    fcc = _FunctionContextCreator('mynamespace', f'mydir{os.sep}subdir')

    functions = [
        Function(
            commands=[
                'function mynamespace:mydir/subdir/conv-reward-function_1',
                'schedule function mynamespace:rewarding-function 2s'
            ],
            function_context=fcc.make_function_context('conv-reward-function')
        ),
        Function(
            commands=[
                'tellraw @a ["", '
                '{"text": "(1/1) ", "color": "gray", "bold": true}, '
                '{"text": "John: ", "color": "yellow", "bold": true}, '
                '{"text": "You earned a reward!", "color": "yellow"}'
                ']'
            ],
            function_context=fcc.make_function_context('conv-reward-function_1')
        ),
    ]

    return MConvTestFixture(file_path, yaml, conv_ctx, conversation, functions)


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
