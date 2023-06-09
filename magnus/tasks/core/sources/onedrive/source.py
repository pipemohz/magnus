"""
One drive data source.
"""
# Python built-in
from datetime import datetime, timedelta
import logging
import pytz
import requests

# msal
import msal

# Environment
from config.environment import MS_LOGIN_API, MS_GRAPH_API, AZURE_APP
from tasks.utils import decode_docx, decode_pdf
from db import cosmos_client
from uuid import uuid4


class OneDriveDS:
    def __init__(self) -> None:
        self.__format = "%Y-%m-%dT%H:%M:%SZ"
        self.__now = datetime.now(pytz.timezone("UTC"))
        self.__yesterday = self.__now - timedelta(days=1)

    def run(self):
        self.__authenticate()
        items = self.__get_items()
        logging.info(f"items:{len(items)}")
        records = self.__build_records(items)
        self.__insert_records(records)

    def __authenticate(self):
        authority = f"{MS_LOGIN_API}/{AZURE_APP['TENANT_ID']}"

        app = msal.ConfidentialClientApplication(
            AZURE_APP["CLIENT_ID"],
            authority=authority,
            client_credential=AZURE_APP["CLIENT_SECRET"],
        )

        result = app.acquire_token_by_username_password(
            scopes=MS_GRAPH_API["SCOPES"],
            username=AZURE_APP["USERNAME"],
            password=AZURE_APP["PASSWORD"],
        )

        if not result:
            raise Exception("Error on authentication.")

        self.__access_token = result["access_token"]
        self.__headers = {"Authorization": f"Bearer {self.__access_token}"}

    def __get_items(self):
        url = (
            f"{MS_GRAPH_API['URL']}/drives/{MS_GRAPH_API['DRIVE_ID']}/items/root/delta"
        )

        params = {"token": self.__yesterday.strftime(self.__format)}

        response = requests.get(url, headers=self.__headers, params=params)
        response.raise_for_status()

        return [item for item in response.json()["value"] if not "folder" in item]

    def __build_records(self, items: list):
        records = list()
        for i, item in enumerate(items):
            logging.info(f"item {i+1}:")
            try:
                data = self.__download_item(item)
                records.append(
                    {
                        "id": str(uuid4()),
                        "web_url": item["webUrl"],
                        "data": data,
                        "created_at": item["createdDateTime"],
                        "updated_at": item["lastModifiedDateTime"],
                    }
                )
            except Exception as error:
                logging.info(
                    f"An error has ocurred on download item {item['id']}: {error}"
                )

        return records

    def __download_item(self, item: dict):
        url = f"{MS_GRAPH_API['URL']}/drives/{MS_GRAPH_API['DRIVE_ID']}/items/{item['id']}/content"

        response = requests.get(url, headers=self.__headers)
        response.raise_for_status()

        if "docx" in item["name"]:
            text = decode_docx(response.content)
        elif "pdf" in item["name"]:
            text = decode_pdf(response.content)
        else:
            raise Exception("Not a valid file type.")

        return text

    def __insert_records(self, records: list[dict]):
        cosmos_client.insert("curriculums", records)
