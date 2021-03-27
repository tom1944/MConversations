import os
import unittest

from mconv.conversation.conversation_context import ConversationContext
from mconv.datapack_updater import DatapackUpdater, ConversationFileLocator


class DatapackUpdaterTest(unittest.TestCase):
    def test_datapack_updater(self):
        datapack_updater = DatapackUpdater('example-datapack')
        datapack_updater.update_conversations_in_datapack()

        files = [os.sep.join(paths) for paths in [
            ['example-datapack', 'data', 'mynamespace', 'functions', 'conv.mcfunction'],
            ['example-datapack', 'data', 'mynamespace', 'functions', 'conv_1.mcfunction'],
            ['example-datapack', 'data', 'mynamespace', 'functions', 'conv_2.mcfunction'],
            ['example-datapack', 'data', 'mynamespace', 'functions', 'conv_3.mcfunction'],
            ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text.mcfunction'],
            ['example-datapack', 'data', 'mynamespace', 'functions', 'mydir', 'conv-with-json-text_1.mcfunction'],
        ]]

        for file in files:
            with self.subTest(f'{file}'):
                self.assertTrue(os.path.isfile(file), f'{file} does not exists')

        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

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
