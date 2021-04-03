import unittest

from mconv.parse_conversation import parse_conversation
from test.fixture import fixture


class ParseConversationTest(unittest.TestCase):
    def test_parse_simple_conversation(self):
        conversation_context, simple_conversation_yaml = fixture.make_simple_conversation_yaml()
        expected_conversation = fixture.make_simple_conversation_object()

        conversation = parse_conversation(conversation_context, simple_conversation_yaml)

        self.assertEqual(expected_conversation.ctx, conversation.ctx)
        self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
        self.assertEqual(expected_conversation.lines, conversation.lines)

    def test_parse_conversation_containing_json_text(self):
        conversation_context, simple_conversation_yaml = fixture.make_conversation_using_json_text_yaml()
        expected_conversation = fixture.make_conversation_using_json_text_object()

        conversation = parse_conversation(conversation_context, simple_conversation_yaml)

        self.assertEqual(expected_conversation.ctx, conversation.ctx)
        self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
        self.assertEqual(expected_conversation.lines, conversation.lines)


if __name__ == '__main__':
    unittest.main()
