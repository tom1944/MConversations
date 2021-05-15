import unittest
from typing import List

from test.fixture.fixture import make_conv_fixtures, MConvTestFixture


class TestCaseWithFixture(unittest.TestCase):
    def setUp(self):
        self.conv_fixtures: List[MConvTestFixture]
        self.conv_fixtures = make_conv_fixtures()
        self.maxDiff = 2000
