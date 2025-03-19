import pathlib
import sys

import pytest
import grpc

from testsuite.databases.pgsql import discover

import handlers.hello_pb2_grpc as hello_services  # noqa: E402, E501

USERVER_CONFIG_HOOKS = ['prepare_service_config']
pytest_plugins = [
    'pytest_userver.plugins.postgresql',
    'pytest_userver.plugins.grpc',
]


@pytest.fixture
def grpc_service(pgsql, grpc_channel, service_client):
    return hello_services.HelloServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def prepare_service_config(grpc_mockserver_endpoint):
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
        'service_template',
        [service_source_dir.joinpath('postgresql/schemas')],
    )
    return pgsql_local_create(list(databases.values()))
