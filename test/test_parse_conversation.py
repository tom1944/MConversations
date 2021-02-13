import unittest

from mconv.parse_conversation import parse_conversation
from test import fixture


class ParseConversationTest(unittest.TestCase):
    def test_parse_simple_conversation(self):
        simple_conversation_yaml = fixture.make_simple_conversation_yaml()

        expected_conversation = fixture.make_simple_conversation_object()

        conversation = parse_conversation('conv1', simple_conversation_yaml)

        self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
        self.assertEqual(expected_conversation.lines, conversation.lines)


if __name__ == '__main__':
    unittest.main()
