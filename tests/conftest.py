import pathlib
import sys

import pytest
import grpc

from testsuite.databases.pgsql import discover

USERVER_CONFIG_HOOKS = ['_prepare_service_config']
pytest_plugins = [
    'pytest_userver.plugins.postgresql',
    'pytest_userver.plugins.grpc',
]


@pytest.fixture(scope='session')
def hello_protos():
    return grpc.protos('hello.proto')


@pytest.fixture(scope='session')
def hello_services():
    return grpc.services('hello.proto')


@pytest.fixture
def grpc_service(pgsql, hello_services, grpc_channel, service_client):
    return hello_services.HelloServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def mock_grpc_hello_session(
        hello_services, grpc_mockserver, create_grpc_mock,
):
    mock = create_grpc_mock(hello_services.HelloServiceServicer)
    hello_services.add_HelloServiceServicer_to_server(
        mock.servicer, grpc_mockserver,
    )
    return mock


@pytest.fixture
def mock_grpc_server(mock_grpc_hello_session):
    with mock_grpc_hello_session.mock() as mock:
        yield mock


@pytest.fixture(scope='session')
def _prepare_service_config(grpc_mockserver_endpoint):
    def patch_config(config, config_vars):
        components = config['components_manager']['components']
        components['hello-client']['endpoint'] = grpc_mockserver_endpoint

    return patch_config


def pytest_configure(config):
    sys.path.append(str(
        pathlib.Path(__file__).parent.parent / 'proto/handlers/'))


@pytest.fixture(scope='session')
def service_source_dir():
    """Path to root directory service."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='session')
def initial_data_path(service_source_dir):
    """Path for find files with data"""
    return [
        service_source_dir / 'postgresql/data',
    ]


@pytest.fixture(scope='session')
def pgsql_local(service_source_dir, pgsql_local_create):
    """Create schemas databases for tests"""
    databases = discover.find_schemas(
        'pg_grpc_service_template',
        [service_source_dir.joinpath('postgresql/schemas')],
    )
    return pgsql_local_create(list(databases.values()))
