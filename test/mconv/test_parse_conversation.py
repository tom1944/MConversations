import unittest

from mconv.parse_conversation import parse_conversation
from test.fixture.test_case_with_fixtures import TestCaseWithFixture


class ParseConversationTest(TestCaseWithFixture):
    def test_parse_conversation(self):

        for conv_fixture in self.conv_fixtures:
            with self.subTest(msg=conv_fixture.conv_ctx.name):
                expected_conversation = conv_fixture.conversation

                conversation = parse_conversation(
                    conv_fixture.conv_ctx,
                    conv_fixture.yaml
                )

                self.assertEqual(expected_conversation.ctx, conversation.ctx)
                self.assertEqual(expected_conversation.speaker_name, conversation.speaker_name)
                self.assertEqual(expected_conversation.lines, conversation.lines)


if __name__ == '__main__':
    unittest.main()
