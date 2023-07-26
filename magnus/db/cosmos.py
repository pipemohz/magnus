"""
Cosmos client
"""
# python built-in
from datetime import datetime

# Azure cosmos
from azure.cosmos import CosmosClient
from azure.cosmos.database import DatabaseProxy

# Environment
from config.environment import COSMOS

MAGNUS_CONTAINER = "cvs"


class Cosmos:
    def __init__(self) -> None:
        self.client = CosmosClient(COSMOS["URI"], COSMOS["KEY"])
        self.database = self.client.get_database_client(COSMOS["NAME"])

    def insert(self, records: list[dict], container_name: str = MAGNUS_CONTAINER):
        container = self.database.get_container_client(container_name)

        for record in records:
            record["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            container.upsert_item(record)

    def get(self, container_name: str = MAGNUS_CONTAINER):
        return [
            item
            for item in self.database.get_container_client(container_name).query_items(
                f"SELECT * from {container_name}", enable_cross_partition_query=True
            )
        ]

    def get_records_with_embedding(self, container_name: str = MAGNUS_CONTAINER):
        return [
            item
            for item in self.database.get_container_client(container_name).query_items(
                f"SELECT * from {container_name} WHERE IS_DEFINED({container_name}.embedding)",
                enable_cross_partition_query=True,
            )
        ]

    def get_embedding_empty(self, container_name: str = MAGNUS_CONTAINER):
        return [
            item
            for item in self.database.get_container_client(container_name).query_items(
                f"SELECT * from {container_name} WHERE NOT IS_DEFINED({container_name}.embedding)",
                enable_cross_partition_query=True,
            )
        ]


class Container:
    def __init__(self, database: DatabaseProxy, container_name: str) -> None:
        self.container_name = container_name
        self.container_proxy = database.get_container_client(container_name)
        self.stmt = f"SELECT * from {self.container_name} "

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
        for expr in exprs:
            self.stmt += expr
        return self
