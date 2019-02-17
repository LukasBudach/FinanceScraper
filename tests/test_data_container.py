import unittest
import logging
import copy

from financescraper.datacontainer import container


class TestTickerData(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.ERROR)
        self.example = container.TickerData('Yahoo')
        self.example.price = 29.99
        self.example.etf = False

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def testEquals(self):
        my_copy = copy.copy(self.example)
        self.assertTrue(self.example == my_copy)
        my_copy.name = 'Different Name'
        self.assertFalse(self.example == my_copy)

    def testStr(self):
        expected = 'No name found: 29.99 USD from Yahoo || ETF: False'
        self.assertEqual(str(self.example), expected)

    def testRepr(self):
        expected = 'TickerData(USD, False, No name found, {}, Yahoo)'.format(29.99)
        self.assertEqual(repr(self.example), expected)

    def testMergeKeepPrice(self):
        to_merge = container.TickerData('IEX')
        to_merge.price = 31.99
        to_merge.etf = True
        to_merge.name = 'Test stock'

        expected = container.TickerData('Yahoo & IEX')
        expected.price = 29.99
        expected.etf = False
        expected.name = 'Test stock'

        self.example.merge(to_merge)
        self.assertTrue(self.example == expected)

    def testMergeChangePrice(self):
        to_merge = container.TickerData('IEX')
        to_merge.price = 31.99
        to_merge.currency = 'EUR'
        to_merge.etf = True
        to_merge.name = 'Test stock'

        expected = container.TickerData('Yahoo & IEX')
        expected.price = 31.99
        expected.currency = 'EUR'
        expected.etf = False
        expected.name = 'Test stock'

        self.example.merge(to_merge)
        self.assertTrue(self.example == expected)


class TestCompanyData(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.ERROR)
        self.example = container.CompanyData('Yahoo')
        self.example.symbol = 'ABC'

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def testEquals(self):
        my_copy = copy.copy(self.example)
        self.assertTrue(self.example == my_copy)
        my_copy.name = 'Different Company'
        self.assertFalse(self.example == my_copy)

    def testStr(self):
        expected = 'ABC: No name found - No website found from Yahoo || sector: No sector found || industry: No ' \
                   'industry found || exchange: No exchange found || description: No description found'
        self.assertEqual(str(self.example), expected)

    def testRepr(self):
        expected = 'CompanyData(No description found, No exchange found, No industry found, No name found, No sector ' \
                   'found, Yahoo, ABC, No website found)'
        self.assertEqual(repr(self.example), expected)

    def testMerge(self):
        to_merge = container.CompanyData('IEX')
        to_merge.name = 'Alphabet Inc.'
        to_merge.description = 'A big corporation.'
        to_merge.website = 'google.com'

        expected = copy.copy(to_merge)
        expected.symbol = 'ABC'
        expected.source = 'Yahoo & IEX'

        self.example.merge(to_merge)
        self.assertTrue(self.example == expected)
