import os
import unittest

from mconv.datapack_updater import DatapackUpdater


class DatapackUpdaterTest(unittest.TestCase):
    def test_datapack_updater(self):
        datapack_updater = DatapackUpdater('example-datapack')
        datapack_updater.create_conversations_in_datapack()

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


if __name__ == '__main__':
    unittest.main()
