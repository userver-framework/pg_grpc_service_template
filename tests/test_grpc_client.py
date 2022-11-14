import pytest


# Start the tests via `make test-debug` or `make test-release`

async def test_grpc_client(hello_protos, mock_grpc_hello, grpc_service):
    @mock_grpc_hello('SayHello')
    async def mock_say_hello(request, context):
        return hello_protos.HelloResponse(
            text=f'Hello, {request.name}!',
        )

    request = hello_protos.HelloRequest(name='userver')
    response = await grpc_service.SayHelloMock(request)
    assert response.text == 'Hello, userver!'
    assert mock_say_hello.times_called == 1
