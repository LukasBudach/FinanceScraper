import unittest

from financescraper import scraper


class TestYahooScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.YahooScraper()

    def tearDown(self):
        self.scraper.close_connection()

    def test_scraper_default_init(self):
        self.assertTrue(self.scraper.use_buffer)
        self.assertEqual(self.scraper.buffer.max_size, 10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 15)
        self.assertEqual(self.scraper.url, 'https://finance.yahoo.com/quote/')

    def test_scraper_set_buffer_size(self):
        self.scraper.set_buffer_size(5)
        self.assertEqual(self.scraper.buffer.max_size, 5)

    def test_scraper_set_holding_time(self):
        self.scraper.set_holding_time(10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 10)


if __name__ == '__main__':
    unittest.main()
