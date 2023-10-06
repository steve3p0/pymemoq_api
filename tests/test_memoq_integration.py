import pytest
import os
import configparser
from src import memoq_soap as mq
from src.memoq_tm import MemoqTm
from src.memoq_tb import MemoqTb

ENVIRONMENT = 'stage'
# ENVIRONMENT = 'prod'


@pytest.fixture(scope="module")
def setup_soap():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the config file path
    config_filename = None
    if ENVIRONMENT == 'stage':
        config_filename = 'memoq.config.stage.ini'
    elif ENVIRONMENT == 'prod':
        config_filename = 'memoq.config.prod.ini'
    config_path = os.path.join(current_dir, '..', 'config', config_filename)  # If memoq.config.ini is inside a config directory

    # Read the configuration directly within the fixture
    config = configparser.ConfigParser()
    config.read(config_path)
    api_url = config.get('API', 'API_URL')
    api_key = config.get('API', 'API_KEY')

    soap_client = mq.MemoqSoap(wsdl_base_url=api_url, api_key=api_key)

    return soap_client


def test_list_tms_integration(setup_soap):
    tm = MemoqTm(setup_soap)
    status, data = tm.list_tms()
    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_get_tm_info_integration(setup_soap):
    guid = "72df1bcf-a1e1-4f50-9fbb-0283dbcbe733"
    tm = MemoqTm(setup_soap)
    status, data = tm.get_tm_info(guid)
    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_list_tbs_integration(setup_soap):
    tb = MemoqTb(setup_soap)
    status, data = tb.list_tbs()
    assert status == 200
    assert data is not None

    # 72df1bcf-a1e1-4f50-9fbb-0283dbcbe733