import unittest
from unittest.mock import Mock

from src import memoq_soap as mq, memoq_tb as tb  # Assuming you've created memoq_tb.py


class TestMemoqTb(unittest.TestCase):

    def setUp(self):
        self.soap_client = Mock(spec=mq.MemoqSoap)
        self.tb_client = tb.MemoqTb(self.soap_client)  # Assuming you've created a MemoqTb class in memoq_tb.py

    def test_init(self):
        self.assertIsInstance(self.tb_client.soap_client, mq.MemoqSoap)

    def test_list_tbs(self):
        # Mock the make_soap_request method to return a tuple (200, "term_base_data")
        self.soap_client.make_soap_request.return_value = (200, "term_base_data")

        status, data = self.tb_client.list_tbs()

        self.assertEqual(status, 200)
        self.assertEqual(data, "term_base_data")


if __name__ == '__main__':
    unittest.main()
