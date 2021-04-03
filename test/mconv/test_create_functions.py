import unittest

from mconv.create_functions import create_functions
from test.fixture import fixture


class CreateFunctionsTest(unittest.TestCase):
    def test_create_functions_from_simple_conversation(self):
        conversation = fixture.make_simple_conversation_object()
        expected_functions = fixture.make_simple_conversation_functions()

        actual_functions = create_functions(conversation)

        self.assertCountEqual(expected_functions, actual_functions)

    def test_create_functions_from_conversation_containing_json_text(self):
        conversation = fixture.make_conversation_using_json_text_object()
        expected_functions = fixture.make_conversation_using_json_text_functions()

        actual_functions = create_functions(conversation)

        self.assertCountEqual(expected_functions, actual_functions)


if __name__ == '__main__':
    unittest.main()
