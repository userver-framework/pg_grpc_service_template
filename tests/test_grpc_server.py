import pytest

from testsuite.databases import pgsql


# Start the tests via `make test-debug` or `make test-release`


async def test_first_time_users(hello_protos, grpc_service):
    request = hello_protos.HelloRequest(name='userver')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hello, userver!\n'


async def test_db_updates(hello_protos, grpc_service):
    request = hello_protos.HelloRequest(name='World')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hello, World!\n'

    request = hello_protos.HelloRequest(name='World')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hi again, World!\n'

    request = hello_protos.HelloRequest(name='World')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hi again, World!\n'


@pytest.mark.pgsql('db-1', files=['initial_data.sql'])
async def test_db_initial_data(hello_protos, grpc_service):
    request = hello_protos.HelloRequest(name='user-from-initial_data.sql')
    response = await grpc_service.SayHello(request)
    assert response.text == 'Hi again, user-from-initial_data.sql!\n'
