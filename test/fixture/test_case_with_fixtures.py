import unittest

from test.fixture.fixture import make_conv_fixtures, MConvTestFixture


class TestCaseWithFixture(unittest.TestCase):
    def setUp(self):
        self.conv_fixtures: MConvTestFixture
        self.conv_fixtures = make_conv_fixtures()
