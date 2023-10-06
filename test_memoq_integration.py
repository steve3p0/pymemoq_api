import pytest
import configparser

import memoq_soap as mq
from memoq_tm import MemoqTm

@pytest.fixture(scope="module")
def setup_clients():
    # Read the configuration directly within the fixture
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_url = config.get('API', 'API_URL')
    api_key = config.get('API', 'API_KEY')

    soap_client = mq.MemoqSoap(wsdl_base_url=api_url, api_key=api_key)
    tm_client = MemoqTm(soap_client)
    return tm_client


def test_get_tm_list_integration(setup_clients):
    status, data = setup_clients.get_tm_list()
    assert status == 200  # Assuming 200 is the success code
    assert data is not None


def test_get_tb_list_integration(setup_clients):
    status, data = setup_clients.get_tb_list()
    assert status == 200  # Assuming 200 is the success code
    assert data is not None  # You might want to add more specific checks here
