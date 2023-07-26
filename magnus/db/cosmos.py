"""
Cosmos client
"""
# python built-in
import json
from datetime import datetime

# Azure cosmos
from azure.cosmos import CosmosClient

# Environment
from config.environment import COSMOS


class Cosmos:
    def __init__(self) -> None:
        self.client = CosmosClient(COSMOS["URI"], COSMOS["KEY"])
        self.database = self.client.get_database_client(COSMOS["NAME"])

    def insert(self, container_name: str, records: list[dict]):
        container = self.database.get_container_client(container_name)

        for record in records:
            record["updated_at"] = datetime.now()
            container.upsert_item(record)

    def get(self, container_name: str):
        return [
            item
            for item in self.database.get_container_client(container_name).query_items(
                f"SELECT * from {container_name}", enable_cross_partition_query=True
            )
        ]

    def get_records_with_embedding(self, container_name: str = "curriculums"):
        return [
            item
            for item in self.database.get_container_client(container_name).query_items(
                f"SELECT * from {container_name} WHERE IS_DEFINED({container_name}.embedding)",
                enable_cross_partition_query=True,
            )
        ]

    def get_embedding_empty(self, container_name: str):
        return [
            item
            for item in self.database.get_container_client(container_name).query_items(
                f"SELECT * from {container_name} WHERE NOT IS_DEFINED({container_name}.embedding)",
                enable_cross_partition_query=True,
            )
        ]
