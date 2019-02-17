import unittest
import logging
import time

from financescraper import scraper


class TestBaseScraperFunctionality(unittest.TestCase):
    def setUp(self):
        # using just any basic scraper as we can't test the abstract base class directly
        self.scraper = scraper.IEXScraper()
        logging.disable(logging.ERROR)

    def tearDown(self):
        self.scraper.close_connection()
        logging.disable(logging.NOTSET)

    def test_scraper_set_buffer_size(self):
        self.scraper.set_buffer_size(5)
        self.assertEqual(self.scraper.buffer.max_size, 5)

    def test_scraper_set_holding_time(self):
        self.scraper.set_holding_time(10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 10)

    def test_get_data_with_buffer(self):
        valid_ticker = 'AAPL'
        start_time = time.time()
        self.scraper._get_data_object(valid_ticker)
        start_time_buffer = end_time = time.time()
        self.scraper._get_data_object(valid_ticker)
        end_time_buffer = time.time()
        self.assertTrue((end_time_buffer - start_time_buffer) < (end_time - start_time))

    def test_get_data_without_buffer(self):
        valid_ticker = 'AAPL'
        self.scraper.use_buffer = False
        self.assertIsNotNone(self.scraper._get_data_object(valid_ticker))


if __name__ == '__main__':
    unittest.main()
