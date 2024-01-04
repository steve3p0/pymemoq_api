import pytest
import os
import configparser
from src import memoq_soap as mq
from src.memoq_tm import MemoqTm
from src.memoq_tb import MemoqTb
from src.memoq_projects import MemoqProjects

# ENVIRONMENT = 'stage'
ENVIRONMENT = 'prod'


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


def test_list_tms(setup_soap):
    tm = MemoqTm(setup_soap)
    status, data = tm.list_tms()
    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_get_tm_info(setup_soap):
    # stage guids
    # guid = "72df1bcf-a1e1-4f50-9fbb-0283dbcbe733"
    # guid = "fc91bbbf-cd9c-41b2-87d7-05672db40e7d"

    # prod guids
    guid = "3353ec0e-5a99-488b-bc78-0005003e2b02"

    tm = MemoqTm(setup_soap)
    status, data = tm.get_tm_info(guid)
    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_list_tbs(setup_soap):
    tb = MemoqTb(setup_soap)
    status, data = tb.list_tbs()
    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_list_projects(setup_soap):
    project_client = MemoqProjects(setup_soap)
    status, data = project_client.list_projects()
    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_list_project_translation_documents(setup_soap):
    project = MemoqProjects(setup_soap)
    guid = "7ac30c94-ee9c-ed11-813e-0050569a4a0a"

    # options = {"some_option": "some_value"}  # Replace with actual options
    # status, data = project.list_project_translation_documents2(guid, options)

    status, data = project.list_project_translation_documents(guid)

    print(f"data: {data}")
    assert status == 200
    assert data is not None


def test_list_project_translation_documents_by_guids_from_file(setup_soap):
    project = MemoqProjects(setup_soap)

    # Open the file containing the project GUIDs
    with open('memoq_project_guids_stage.txt', 'r') as file:
        project_guids = file.readlines()

    docs_found = False
    # Loop through each project GUID and list the project translation documents
    for guid in project_guids:
        guid = guid.strip()  # Remove any leading/trailing whitespace or newlines
        options = {"some_option": "some_value"}  # Replace with actual options

        status, data = project.list_project_translation_documents2(guid, options)

        # if 'Status: 500' in data:
        #         docs_found = True

        print(f"---------------------------------------------------------------------------------------")
        print(f"Project Guid: {guid}")
        print(f"Status: {status}")
        print(f"Data for project {guid}: {data}")
        # assert status == 200
        # assert data is not None

    # assert docs_found == True


# @pytest.mark.skipif(sys.version_info < (3,3), reason="requires python3.3")
def test_list_project_translation_documents2(setup_soap):
    project = MemoqProjects(setup_soap)
    guid = "7ac30c94-ee9c-ed11-813e-0050569a4a0a"

    # options = {"some_option": "some_value"}  # Replace with actual options
    # status, data = project.list_project_translation_documents2(guid, options)

    status, data = project.list_project_translation_documents2(guid)

    print(f"data: {data}")
    assert status == 200
    assert data is not None

