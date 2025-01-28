#include "hello_client.hpp"

#include <fmt/format.h>

#include <userver/yaml_config/merge_schemas.hpp>

namespace service_template {

std::string HelloClient::SayHello(std::string name) {
  handlers::api::HelloRequest request;
  request.set_name(std::move(name));

  // Perform RPC by sending the request and receiving the response.
  auto response = client_.SayHello(request);

  return std::move(*response.mutable_text());
}

userver::yaml_config::Schema HelloClient::GetStaticConfigSchema() {
  return userver::yaml_config::MergeSchemas<
      userver::components::LoggableComponentBase>(R"(
type: object
description: >
    a user-defined wrapper around api::GreeterServiceClient that provides
    a simplified interface.
additionalProperties: false
properties:
    endpoint:
        type: string
        description: >
            Some other service endpoint (URI). 
)");
}

void AppendHelloClient(userver::components::ComponentList& component_list) {
  component_list.Append<HelloClient>();
}

}  // namespace service_template
