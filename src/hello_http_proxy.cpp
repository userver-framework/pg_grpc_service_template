#include "hello_http_proxy.hpp"

#include <fmt/format.h>

#include <userver/clients/dns/component.hpp>
#include <userver/server/handlers/http_handler_base.hpp>
#include <userver/storages/postgres/cluster.hpp>
#include <userver/storages/postgres/component.hpp>
#include <userver/utils/assert.hpp>

namespace pg_grpc_service_template {

std::string HelloHttpProxy::HandleRequestThrow(
    const userver::server::http::HttpRequest& request,
    userver::server::request::RequestContext&) const {
  return hello_client_.SayHello(request.GetArg("name"));
}

void AppendHelloHttpProxy(userver::components::ComponentList& component_list) {
  component_list.Append<HelloHttpProxy>();
}

}  // namespace pg_grpc_service_template
