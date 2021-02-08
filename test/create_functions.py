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
                    'schedule function mynamespace:path/to/dir/conv1_1 0',
                    'schedule function mynamespace:path/to/dir/conv1_2 2',
                    'schedule function mynamespace:path/to/dir/conv1_3 5',
                ]
            ),
            Function(
                name='conv1_1',
                prefix=function_prefix,
                commands=[
                    'tellraw @s "(1/3) Erik: Hello!"'
                ]
            ),
            Function(
                name='conv1_2',
                prefix=function_prefix,
                commands=[
                    'tellraw @s "(2/3) Erik: This is a very long text that requires 3 seconds of reading time"'
                ]
            ),
            Function(
                name='conv1_3',
                prefix=function_prefix,
                commands=[
                    'tellraw @s "(3/3) Erik: This is the end..."'
                ]
            ),
        ]

        actual_functions = create_functions(conversation)

        self.assertEqual(expected_functions, actual_functions)


if __name__ == '__main__':
    unittest.main()
