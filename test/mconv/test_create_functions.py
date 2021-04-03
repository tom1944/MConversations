import unittest

from mconv.create_functions import create_functions
from test.fixture.test_case_with_fixtures import TestCaseWithFixture


class CreateFunctionsTest(TestCaseWithFixture):
    def test_create_functions(self):
        for conv_fixture in self.conv_fixtures:
            with self.subTest(msg=conv_fixture.conv_ctx.name):
                actual_functions = create_functions(conv_fixture.conversation)
                self.assertCountEqual(conv_fixture.functions, actual_functions)


if __name__ == '__main__':
    unittest.main()
