import unittest

from mconv.parse_conversation import parse_conversation
from test import fixture


class ParseConversationTest(unittest.TestCase):
    def test_parse_simple_conversation(self):
        function_prefix, simple_conversation_yaml = fixture.make_simple_conversation_yaml()
        expected_conversation = fixture.make_simple_conversation_object()

        conversation = parse_conversation('conv1', simple_conversation_yaml, function_prefix)

        self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
        self.assertEqual(expected_conversation.function_prefix, conversation.function_prefix)
        self.assertEqual(expected_conversation.lines, conversation.lines)

    def test_parse_conversation_containing_json_text(self):
        function_prefix, simple_conversation_yaml = fixture.make_conversation_using_json_text_yaml()
        expected_conversation = fixture.make_conversation_using_json_text_object()

        conversation = parse_conversation('conv2', simple_conversation_yaml, function_prefix)

        self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
        self.assertEqual(expected_conversation.function_prefix, conversation.function_prefix)
        self.assertEqual(expected_conversation.lines, conversation.lines)


if __name__ == '__main__':
    unittest.main()
