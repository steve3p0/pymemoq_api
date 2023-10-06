import pytest
import os
import configparser
from src import memoq_soap as mq
from src.memoq_tm import MemoqTm

ENVIRONMENT = 'stage'


@pytest.fixture(scope="module")
def setup_clients():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the config file path
    config_filename = None
    if ENVIRONMENT == 'stage':
        config_filename = 'config.stage.ini'
    elif ENVIRONMENT == 'prod':
        config_filename = 'config.prod.ini'
    config_path = os.path.join(current_dir, '..', 'config', config_filename)  # If config.ini is inside a config directory

    # Read the configuration directly within the fixture
    config = configparser.ConfigParser()
    config.read(config_path)
    api_url = config.get('API', 'API_URL')
    api_key = config.get('API', 'API_KEY')

    soap_client = mq.MemoqSoap(wsdl_base_url=api_url, api_key=api_key)
    tm_client = MemoqTm(soap_client)
    return tm_client


def test_get_tm_list_integration(setup_clients):
    status, data = setup_clients.list_tms()
    assert status == 200  # Assuming 200 is the success code
    assert data is not None


def test_get_tb_list_integration(setup_clients):
    status, data = setup_clients.list_tbs()
    assert status == 200  # Assuming 200 is the success code
    assert data is not None  # You might want to add more specific checks here
