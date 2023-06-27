"""
Cosmos client
"""

# Azure cosmos
from azure.cosmos import CosmosClient

# Environment
from config.environment import COSMOS


class Cosmos:
    def __init__(self) -> None:
        self.client = CosmosClient(COSMOS["URI"], COSMOS["KEY"])

    def insert(self, container_name: str, records: list[dict]):
        database = self.client.get_database_client(COSMOS["NAME"])
        container = database.get_container_client(container_name)

        for record in records:
            container.upsert_item(record)
