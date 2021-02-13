import unittest

from mconv.conversation import Conversation
from mconv.create_functions import create_functions
from mconv.function import Function
from mconv.line import Line


class CreateFunctionsTest(unittest.TestCase):
    def test_create_functions(self):
        conversation = Conversation(
            'conv1',
            'mynamespace:path/to/dir/',
            'Erik',
            [
                Line('Hello!', speak_time=2),
                Line('This is a very long text that requires 3 seconds of reading time', speak_time=3),
                Line('This is the end...', speak_time=2)
            ]
        )

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
                    'tellraw @a ["",'
                    '{"text":"(1/3) ","bold":true,"color":"gray"},'
                    '{"text":"Erik: ","bold":true,"color":"yellow"},'
                    '{"text":"Hello!","color":"yellow"}'
                    ']'
                ]
            ),
            Function(
                name='conv1_2',
                prefix=function_prefix,
                commands=[
                    'tellraw @a ["",'
                    '{"text":"(2/3) ","bold":true,"color":"gray"},'
                    '{"text":"Erik: ","bold":true,"color":"yellow"},'
                    '{"text":"This is a very long text that requires 3 seconds of reading time","color":"yellow"}'
                    ']'
                ]
            ),
            Function(
                name='conv1_3',
                prefix=function_prefix,
                commands=[
                    'tellraw @a ["",'
                    '{"text":"(3/3) ","bold":true,"color":"gray"},'
                    '{"text":"Erik: ","bold":true,"color":"yellow"},'
                    '{"text":"This is the end...","color":"yellow"}'
                    ']'
                ]
            ),
        ]

        actual_functions = create_functions(conversation)

        for expected, actual in zip(expected_functions, actual_functions):
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
