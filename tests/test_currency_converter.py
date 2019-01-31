import unittest
import logging

from financescraper import conversions, scraper


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.usd_converter = conversions.CurrencyConverter('USD')
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_converter_init(self):
        self.assertEqual(self.usd_converter.target_currency_code, 'USD')
        self.assertTrue(self.usd_converter.use_buffer)
        self.assertEqual(self.usd_converter.buffer.max_size, 10)
        self.assertEqual(self.usd_converter.buffer.max_holding_time, 1800)
        self.assertEqual(type(self.usd_converter.yahoo_scraper), scraper.YahooScraper)

    def test_converter_set_buffer_size(self):
        self.usd_converter.set_buffer_size(5)
        self.assertEqual(self.usd_converter.buffer.max_size, 5)

    def test_converter_set_holding_time(self):
        self.usd_converter.set_holding_time(10)
        self.assertEqual(self.usd_converter.buffer.max_holding_time, 10)

    def test_converter_convert(self):
        self.assertEqual(self.usd_converter.convert('USD', 1), 1)
        self.assertEqual(type(self.usd_converter.convert('EUR', 1)), float)
        self.assertIsNone(self.usd_converter.convert('INVALID', 1))


if __name__ == '__main__':
    unittest.main()
