import unittest
import time
import logging

from financescraper.datacontainer import circular_buffer


class TestCircularBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer = circular_buffer.CircularBuffer(2, 1)
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_buffer_init(self):
        self.assertEqual(self.buffer.max_size, 2)
        self.assertEqual(self.buffer.max_holding_time, 1)
        self.assertListEqual(self.buffer.key_list, [])
        self.assertDictEqual(self.buffer.dictionary, {})
        self.assertDictEqual(self.buffer.timestamps, {})

    def test_buffer_set_max_size(self):
        self.buffer.set_size(4)
        self.assertEqual(self.buffer.max_size, 4)

    def test_buffer_set_max_holding_time(self):
        self.buffer.set_holding_time(4)
        self.assertEqual(self.buffer.max_holding_time, 4)

    def test_buffer_timestamp(self):
        self.buffer.add('A', 1)
        self.assertAlmostEqual(self.buffer.timestamps['A'], time.time())

    def test_buffer_add_element(self):
        obj = {
            'A': 1,
            'B': 2
        }
        self.buffer.add('A', obj['A'])
        self.assertDictEqual(self.buffer.dictionary, {'A': obj['A']})
        self.assertListEqual(self.buffer.key_list, ['A'])

        self.buffer.add('B', obj['B'])
        self.assertDictEqual(self.buffer.dictionary, obj)
        self.assertListEqual(self.buffer.key_list, ['A', 'B'])

    def test_buffer_get_element(self):
        obj = {
            'A': 1,
            'B': 2
        }
        self.buffer.add('A', obj['A'])
        self.buffer.add('B', obj['B'])

        self.assertEqual(self.buffer.get('A'), obj['A'])
        self.assertNotEqual(self.buffer.get('A'), obj['B'])

    def test_buffer_delete_element(self):
        obj = {
            'A': 1,
            'B': 2
        }
        expected = {'B': 2}

        self.buffer.add('A', obj['A'])
        self.buffer.add('B', obj['B'])

        self.buffer.delete('A')
        self.assertDictEqual(self.buffer.dictionary, expected)

    def test_buffer_clear(self):
        obj = {
            'A': 1,
            'B': 2
        }
        expected = {}

        self.buffer.add('A', obj['A'])
        self.buffer.add('B', obj['B'])

        self.buffer.clear()
        self.assertDictEqual(self.buffer.dictionary, expected)

    def test_buffer_overflow(self):
        obj = {
            'A': 1,
            'B': 2,
            'C': 3
        }
        expected = {
            'B': 2,
            'C': 3
        }
        self.buffer.add('A', obj['A'])
        self.buffer.add('B', obj['B'])
        self.buffer.add('C', obj['C'])

        self.assertDictEqual(self.buffer.dictionary, expected)
        self.assertNotEqual(self.buffer.dictionary, obj)

    def test_buffer_refresh(self):
        obj = {
            'A': 1,
            'B': 2,
            'C': 3
        }
        expected = {
            'A': 1,
            'C': 3
        }
        
        self.buffer.add('A', obj['A'])
        self.buffer.add('B', obj['B'])
        self.buffer.refresh('A')
        self.buffer.add('C', obj['C'])

        self.assertDictEqual(self.buffer.dictionary, expected)
        self.assertNotEqual(self.buffer.dictionary, obj)


if __name__ == '__main__':
    unittest.main()
