import unittest

from mconv.create_functions import create_functions
from mconv.function import Function
from mconv.parse_conversation import parse_conversation


class MConvTest(unittest.TestCase):
    def test_simple_conversation(self):
        simple_conversation_str = '\n'.join([
            'function-prefix: mynamespace:path/to/dir/',
            'speaker-name: Erik',
            'default-speak-time-sec: 2',
            'conversation:',
            '  - say: Hello!',
            '  - say: This is a very long text that requires 3 seconds of reading time',
            '    speak-time-sec: 3',
            '  - say: This is the end...',
        ])

        function_prefix = 'mynamespace:path/to/dir/'

        expected_functions = [
            Function(
                name='conv1',
                prefix=function_prefix,
                commands=[
                    'function mynamespace:path/to/dir/conv1_1',
                    'schedule function mynamespace:path/to/dir/conv1_2 2s',
                    'schedule function mynamespace:path/to/dir/conv1_3 5s',
                ]
            ),
            Function(
                name='conv1_1',
                prefix=function_prefix,
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
                prefix=function_prefix,
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
                prefix=function_prefix,
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(3/3) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "This is the end...", "color": "yellow"}'
                    ']'
                ]
            ),
        ]

        conversation = parse_conversation("conv1", simple_conversation_str)
        actual_functions = create_functions(conversation)

        self.assertEqual(expected_functions, actual_functions)
