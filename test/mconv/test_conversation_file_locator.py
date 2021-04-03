import unittest

from mconv.conversion_locator import ConversationFileLocator
from test.fixture.test_case_with_fixtures import TestCaseWithFixture


class ConversationFileLocatorTest(TestCaseWithFixture):
    def test_conversation_file_locator(self):
        conversation_file_locator = ConversationFileLocator('example-datapack')
        expected_contexts = [conv.conv_ctx for conv in self.conv_fixtures]

        actual_contexts = conversation_file_locator.locate_conversations_in_datapack()

        self.assertCountEqual(
            expected_contexts,
            actual_contexts,
        )


if __name__ == '__main__':
    unittest.main()
