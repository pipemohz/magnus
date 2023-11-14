"""
Cosmos client
"""
# Azure cosmos
from azure.cosmos import CosmosClient
from azure.cosmos.database import DatabaseProxy

# Project packages
from config.environment import COSMOS

MAGNUS_CONTAINER = "curriculumsV2"


class Cosmos:
    def __init__(self) -> None:
        self.client = CosmosClient(COSMOS["URI"], COSMOS["KEY"])
        self.database = self.client.get_database_client(COSMOS["NAME"])

    def insert(self, records: list[dict], container_name: str = MAGNUS_CONTAINER):
        from tasks.utils import local_now

        container = self.database.get_container_client(container_name)

        for record in records:
            container.upsert_item(record)

    def get(self, query: str = "SELECT * FROM", container_name: str = MAGNUS_CONTAINER):
        return Container(self.database, query, container_name)


class Container:
    def __init__(
        self, database: DatabaseProxy, query: str, container_name: str
    ) -> None:
        self.container_name = container_name
        self.container_proxy = database.get_container_client(container_name)
        self.stmt = f"{query} {self.container_name} AS container "

    def all(self):
        return [
            item
            for item in self.container_proxy.query_items(
                self.stmt,
                enable_cross_partition_query=True,
            )
        ]

    def first(self):
        return self.all()[0]

    def where(self, *exprs):
        self.stmt += f"WHERE {' '.join(exprs)}"
        return self
