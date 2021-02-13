import unittest

from mconv.create_functions import create_functions
from mconv.parse_conversation import parse_conversation
from test import fixture


class MConvTest(unittest.TestCase):
    def test_simple_conversation(self):
        simple_conversation_yaml = fixture.make_simple_conversation_yaml()
        expected_functions = fixture.make_simple_conversation_functions()

        conversation = parse_conversation("conv1", simple_conversation_yaml)
        actual_functions = create_functions(conversation)

        self.assertCountEqual(expected_functions, actual_functions)
