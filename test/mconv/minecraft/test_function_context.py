import os
import unittest

from mconv.minecraft_lang.function_context import FunctionContext


class FunctionContextTest(unittest.TestCase):
    def test_function_context(self):
        function_context = FunctionContext('mynamespace', '', 'conv')

        self.assertEqual('mynamespace:conv', function_context.as_qualified_function_name())
        self.assertEqual('conv.mcfunction', function_context.as_function_file_name())
        self.assertEqual(
            os.path.join('data', 'mynamespace', 'functions'),
            function_context.as_path_to_function_file()
        )

    def test_function_context_with_path_in_functions_dir(self):
        function_contexts = [
            FunctionContext('mynamespace', 'mydir', 'conv-with-json-text'),
            FunctionContext('mynamespace', '\\mydir\\', 'conv-with-json-text'),
        ]

        for function_context in function_contexts:
            with self.subTest():
                self.assertEqual('mynamespace:mydir/conv-with-json-text', function_context.as_qualified_function_name())
                self.assertEqual(
                    os.path.join('data', 'mynamespace', 'functions', 'mydir'),
                    function_context.as_path_to_function_file()
                )


if __name__ == '__main__':
    unittest.main()
