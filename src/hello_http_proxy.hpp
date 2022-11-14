#pragma once

#include <userver/components/component_list.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

#include "hello_client.hpp"

namespace pg_grpc_service_template {

class HelloHttpProxy final : public userver::server::handlers::HttpHandlerBase {
 public:
  static constexpr std::string_view kName = "handler-hello-http-proxy";

  HelloHttpProxy(const userver::components::ComponentConfig& config,
                 const userver::components::ComponentContext& context)
      : userver::server::handlers::HttpHandlerBase(config, context),
        hello_client_(context.FindComponent<HelloClient>()) {}

  std::string HandleRequestThrow(
      const userver::server::http::HttpRequest& request,
      userver::server::request::RequestContext&) const override;

 private:
  HelloClient& hello_client_;
};

void AppendHelloHttpProxy(userver::components::ComponentList& component_list);

}  // namespace pg_grpc_service_template
