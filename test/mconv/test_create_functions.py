import unittest

from mconv.conversation.conversation import Conversation
from mconv.conversation.conversation_context import ConversationContext
from mconv.conversation.line import FunctionLine, TextLine
from mconv.create_functions import create_functions
from mconv.minecraft_lang.function import Function
from mconv.minecraft_lang.function_context import FunctionContext
from test.fixture.test_case_with_fixtures import TestCaseWithFixture


class CreateFunctionsTest(TestCaseWithFixture):
    def test_create_functions(self):
        for conv_fixture in self.conv_fixtures:
            with self.subTest(msg=conv_fixture.conv_ctx.name):
                actual_functions = create_functions(conv_fixture.conversation)
                self.assertCountEqual(conv_fixture.functions, actual_functions)

    def test_function_on_beginning_of_conv(self):
        conv_ctx = ConversationContext('namespace', '', 'conv-name')
        conversation = Conversation(
            conv_ctx,
            'Erik',
            [
                FunctionLine('other-namespace:reward-function'),
                TextLine('You got reward!', speak_time=5)
            ]
        )

        expected_functions = [
            Function(
                commands=[
                    'execute if score %talk_lock zzz_mconv matches 0 run function'
                    ' namespace:conv-name_no_lock'
                ],
                function_context=FunctionContext('namespace', '', 'conv-name')
            ),
            Function(
                commands=[
                    'function zzz_mconv:lock_talk_lock',
                    'function other-namespace:reward-function',
                    'function namespace:conv-name_1',
                    'function zzz_mconv:free_talk_lock',
                ],
                function_context=FunctionContext('namespace', '', 'conv-name_no_lock')
            ),
            Function(
                commands=[
                    'tellraw @a ["", '
                    '{"text": "(1/1) ", "color": "gray", "bold": true}, '
                    '{"text": "Erik: ", "color": "yellow", "bold": true}, '
                    '{"text": "You got reward!", "color": "yellow"}'
                    ']'
                ],
                function_context=FunctionContext('namespace', '', 'conv-name_1')
            )
        ]

        actual_functions = create_functions(conversation)

        self.assertCountEqual(expected_functions, actual_functions)


if __name__ == '__main__':
    unittest.main()
