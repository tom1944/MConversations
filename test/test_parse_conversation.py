import unittest

from mconv.conversation import Conversation
from mconv.line import Line
from mconv.parse_conversation import parse_conversation


class ParseConversationTest(unittest.TestCase):
    def test_parse_simple_conversation(self):
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

        expected_conversation = Conversation(
            'conv1',
            'mynamespace:path/to/dir/',
            'Erik',
            [
                Line('Hello!', speak_time=2),
                Line('This is a very long text that requires 3 seconds of reading time', speak_time=3),
                Line('This is the end...', speak_time=2)
            ]
        )

        conversation = parse_conversation('conv1', simple_conversation_str)

        self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
        self.assertEqual(expected_conversation.lines, conversation.lines)


if __name__ == '__main__':
    unittest.main()
