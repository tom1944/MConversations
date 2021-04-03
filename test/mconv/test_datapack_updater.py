import os
import unittest

from mconv.datapack_updater import DatapackUpdater
from test.fixture.fixture import make_list_of_generated_function_files


class DatapackUpdaterTest(unittest.TestCase):
    def test_datapack_updater(self):
        datapack_updater = DatapackUpdater('example-datapack')
        datapack_updater.update_conversations_in_datapack()

        files = make_list_of_generated_function_files()

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
