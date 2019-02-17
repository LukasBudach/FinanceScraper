import unittest
import logging
import time

from financescraper import scraper


class TestFinanceScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.FinanceScraper()
        self.valid_ticker = 'AAPL'
        self.iex_invalid_ticker = 'TL0.F'
        self.invalid_ticker = 'AAAA'
        logging.disable(logging.ERROR)

    def tearDown(self):
        del self.scraper
        logging.disable(logging.NOTSET)

    def test_scraper_default_init(self):
        self.assertTrue(self.scraper.use_buffer)
        self.assertEqual(self.scraper.buffer.max_size, 10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 15)
        self.assertIsNone(self.scraper.url)

    def test_set_buffer_size(self):
        self.scraper.set_buffer_size(5)
        idx = 0
        while idx < self.scraper.scraper.__len__():
            self.assertEqual(self.scraper.scraper.get(str(idx)).buffer.max_size, 5)
            idx += 1

    def test_set_holding_time(self):
        self.scraper.set_holding_time(5)
        idx = 0
        while idx < self.scraper.scraper.__len__():
            self.assertEqual(self.scraper.scraper.get(str(idx)).buffer.max_holding_time, 5)
            idx += 1

    def test_set_approach(self):
        self.scraper.set_approach(scraper.ScraperApproach.FAST)
        self.assertEqual(self.scraper.approach, scraper.ScraperApproach.FAST)

    # need to make sure, that the scraper are getting slower the further down one goes
    def test_scraper_order(self):
        idx = 0
        valid_ticker = 'AAPL'
        # make sure that stocks are always re-fetched
        self.scraper.set_holding_time(0)
        while idx < (self.scraper.scraper.__len__() - 1):
            start_faster = time.time()
            self.scraper.scraper.get(str(idx)).get_data(valid_ticker)
            start_slower = end_faster = time.time()
            self.scraper.scraper.get(str(idx + 1)).get_data(valid_ticker)
            end_slower = time.time()
            self.assertTrue((end_faster - start_faster) < (end_slower - start_slower), 'Scraper at %d is slower than'
                                                                                       'scraper at %d' % (idx, idx+1))
            idx += 1

    def test_get_data_fast(self):
        self.scraper.set_approach(scraper.ScraperApproach.FAST)

        response = self.scraper.get_data(self.valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertEqual(type(response.price), float)

        response = self.scraper.get_data(self.iex_invalid_ticker)
        self.assertIsNone(response)

        response = self.scraper.get_data(self.invalid_ticker)
        self.assertIsNone(response)

    def test_get_data_balanced(self):
        self.scraper.set_approach(scraper.ScraperApproach.BALANCED)

        response = self.scraper.get_data(self.valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertEqual(type(response.price), float)

        response = self.scraper.get_data(self.iex_invalid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'Yahoo')
        self.assertEqual(type(response.price), float)

        response = self.scraper.get_data(self.invalid_ticker)
        self.assertIsNone(response)

    def test_get_data_thorough(self):
        # only one of your current sources provides incomplete data, so this test is the same as the balanced one
        self.scraper.set_approach(scraper.ScraperApproach.THOROUGH)

        response = self.scraper.get_data(self.valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertEqual(type(response.price), float)

        response = self.scraper.get_data(self.iex_invalid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'Yahoo')
        self.assertEqual(type(response.price), float)

        response = self.scraper.get_data(self.invalid_ticker)
        self.assertIsNone(response)

    def test_get_company_data_fast(self):
        self.scraper.set_approach(scraper.ScraperApproach.FAST)

        response = self.scraper.get_company_data(self.valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertNotEqual(response.name, 'No name found')
        self.assertEqual(response.symbol, self.valid_ticker)

        response = self.scraper.get_company_data(self.iex_invalid_ticker)
        self.assertIsNone(response)

        response = self.scraper.get_company_data(self.invalid_ticker)
        self.assertIsNone(response)

    def test_get_company_data_balanced(self):
        self.scraper.set_approach(scraper.ScraperApproach.BALANCED)

        response = self.scraper.get_company_data(self.valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertNotEqual(response.name, 'No name found')
        self.assertEqual(response.symbol, self.valid_ticker)

        response = self.scraper.get_company_data(self.iex_invalid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'Yahoo')
        self.assertNotEqual(response.name, 'No name found')
        self.assertEqual(response.symbol, self.iex_invalid_ticker)

        response = self.scraper.get_company_data(self.invalid_ticker)
        self.assertIsNone(response)

    def test_get_company_data_thorough(self):
        # only one of your current sources provides incomplete data, so this test is the same as the balanced one
        self.scraper.set_approach(scraper.ScraperApproach.THOROUGH)

        response = self.scraper.get_company_data(self.valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertNotEqual(response.name, 'No name found')
        self.assertEqual(response.symbol, self.valid_ticker)

        response = self.scraper.get_company_data(self.iex_invalid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'Yahoo')
        self.assertNotEqual(response.name, 'No name found')
        self.assertEqual(response.symbol, self.iex_invalid_ticker)

        response = self.scraper.get_company_data(self.invalid_ticker)
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
