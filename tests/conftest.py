import pathlib
import sys

import pytest
import grpc

from testsuite.databases.pgsql import discover

pytest_plugins = [
    'pytest_userver.plugins',
    'pytest_userver.plugins.samples',
    'pytest_userver.plugins.grpc',
    'testsuite.databases.pgsql.pytest_plugin',
]


@pytest.fixture(scope='session')
def hello_protos():
    return grpc.protos('hello.proto')


@pytest.fixture(scope='session')
def hello_services():
    return grpc.services('hello.proto')


@pytest.fixture
def grpc_service(hello_services, grpc_channel, service_client):
    return hello_services.HelloServiceStub(grpc_channel)


def pytest_configure(config):
    sys.path.append(str(
        pathlib.Path(__file__).parent.parent / 'proto/handlers/'))


@pytest.fixture(scope='session')
def root_dir():
    """Path to root directory service."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='session')
def initial_data_path(root_dir):
    """Path for find files with data"""
    return [
        root_dir / 'postgresql/data',
    ]


@pytest.fixture(scope='session')
def pgsql_local(root_dir, pgsql_local_create):
    """Create schemas databases for tests"""
    databases = discover.find_schemas(
        'pg_grpc_service_template',  # service name that goes to the DB connection
        [root_dir.joinpath('postgresql/schemas')],
    )
    return pgsql_local_create(list(databases.values()))


@pytest.fixture
def client_deps(pgsql):
    pass
