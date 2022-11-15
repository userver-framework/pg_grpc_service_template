#include "hello.hpp"

#include <fmt/format.h>

#include <userver/clients/dns/component.hpp>
#include <userver/storages/postgres/cluster.hpp>
#include <userver/utils/assert.hpp>

namespace pg_grpc_service_template {

void Hello::SayHello(handlers::api::HelloServiceBase::SayHelloCall& call,
                     handlers::api::HelloRequest&& request) {
  auto name = request.name();

  auto user_type = UserType::kFirstTime;
  if (!name.empty()) {
    auto result = pg_cluster_->Execute(
        userver::storages::postgres::ClusterHostType::kMaster,
        "INSERT INTO hello_schema.users(name, count) VALUES($1, 1) "
        "ON CONFLICT (name) "
        "DO UPDATE SET count = users.count + 1 "
        "RETURNING users.count",
        name);

    if (result.AsSingleRow<int>() > 1) {
      user_type = UserType::kKnown;
    }
  }
  if (name.substr(0, 5) == "mock_") {
    name = client_.SayHello(name.substr(5));
  }
  handlers::api::HelloResponse response;
  response.set_text(pg_grpc_service_template::SayHelloTo(name, user_type));
  call.Finish(response);
}

std::string SayHelloTo(std::string_view name, UserType type) {
  if (name.empty()) {
    name = "unknown user";
  }

  switch (type) {
    case UserType::kFirstTime:
      return fmt::format("Hello, {}!\n", name);
    case UserType::kKnown:
      return fmt::format("Hi again, {}!\n", name);
  }

  UASSERT(false);
}

void AppendHello(userver::components::ComponentList& component_list) {
  component_list.Append<Hello>();
  component_list.Append<userver::components::Postgres>("postgres-db-1");
  component_list.Append<userver::clients::dns::Component>();
}

}  // namespace pg_grpc_service_template
