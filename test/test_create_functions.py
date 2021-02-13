import unittest

from mconv.create_functions import create_functions
from test import fixture


class CreateFunctionsTest(unittest.TestCase):
    def test_create_functions(self):
        conversation = fixture.make_simple_conversation_object()
        expected_functions = fixture.make_simple_conversation_functions()

        actual_functions = create_functions(conversation)

        self.assertCountEqual(expected_functions, actual_functions)


if __name__ == '__main__':
    unittest.main()
