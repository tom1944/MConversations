import unittest

from mconv.conversation.conversation_context import ConversationContext
from mconv.conversion_locator import ConversationFileLocator


class ConversationFileLocatorTest(unittest.TestCase):
    def test_conversation_file_locator(self):
        conversation_file_locator = ConversationFileLocator('example-datapack')
        expected_contexts = [
            ConversationContext('mynamespace', '', 'conv'),
            ConversationContext('mynamespace', 'mydir', 'conv-with-json-text')
        ]

        actual_contexts = conversation_file_locator.locate_conversations_in_datapack()

        self.assertCountEqual(
            expected_contexts,
            actual_contexts,
        )


if __name__ == '__main__':
    unittest.main()
