import os
import unittest

from mconv.conversation.conversation_context import ConversationContext


class ConversationContextTest(unittest.TestCase):
    def test_conversation_context(self):
        ctx = ConversationContext('namespace', 'dir', 'conv')
        expected_path = os.path.join('data', 'namespace', 'functions', 'dir', 'conv.yaml')
        self.assertEqual(expected_path, ctx.as_path_in_datapack())
