"""
One drive data source.
"""
# Python built-in
from datetime import timedelta
import logging
import requests

# msal
import msal

# Project packages
from db import cosmos_client
from config.environment import MS_LOGIN_API, MS_GRAPH_API, AZURE_APP
from tasks.utils import decode_docx, decode_pdf, local_now


class OneDriveDS:
    def __init__(self) -> None:
        self.__format = "%Y-%m-%dT%H:%M:%SZ"
        self.__now = local_now()
        self.__yesterday = self.__now - timedelta(days=2)

    def run(self):
        self.__authenticate()
        items = self.__get_items()
        logging.info(f"Number of items to upload:{len(items)}")
        records = self.__build_records(items)
        logging.info(f"Number of records downloaded:{len(records)}")
        self.__insert_records(records)
        logging.info(f"Number of records uploaded:{len(records)}")

    def __authenticate(self):
        authority = f"{MS_LOGIN_API}/{AZURE_APP['TENANT_ID']}"

        app = msal.ConfidentialClientApplication(
            AZURE_APP["CLIENT_ID"],
            authority=authority,
            client_credential=AZURE_APP["CLIENT_SECRET"],
        )

        result = app.acquire_token_silent(scopes=MS_GRAPH_API["SCOPES"], account=None)

        if not result:
            logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
            result = app.acquire_token_for_client(scopes=MS_GRAPH_API["SCOPES"])

        # result = app.acquire_token_by_username_password(
        #     scopes=MS_GRAPH_API["SCOPES"],
        #     username=AZURE_APP["USERNAME"],
        #     password=AZURE_APP["PASSWORD"],
        # )

        if not result:
            raise Exception("Error on authentication.")

        self.__access_token = result["access_token"]
        self.__headers = {"Authorization": f"Bearer {self.__access_token}"}

    def __get_items(self):
        # url = f"{MS_GRAPH_API['URL']}/drives/{MS_GRAPH_API['DRIVE_ID']}/items/{MS_GRAPH_API['FOLDER_ID']}/delta"
        url = f"{MS_GRAPH_API['URL']}/drives/{MS_GRAPH_API['DRIVE_ID']}/items/root/delta"

        params = {"token": self.__yesterday.strftime(self.__format)}
        response = requests.get(url, headers=self.__headers, params=params)
        response.raise_for_status()
        results = []

        while True:    
            data = response.json()
            __ = [item for item in data["value"] if not "folder" in item]
            results.extend(__)

            if "@odata.nextLink" in data:
                url = data["@odata.nextLink"]
                response = requests.get(url, headers=self.__headers)
                response.raise_for_status()
            else:
                break

        return results

    def __build_records(self, items: list):
        records = list()
        
        cosmos_records = cosmos_client.get(query="SELECT container.id FROM").all()
        cosmos_id_records = [c["id"] for c in cosmos_records]
        items = [i for i in items if i["id"] in cosmos_id_records]

        for i, item in enumerate(items):

            if item.get("name") == None:
                continue
            
            logging.info(f"item {i+1}:")
            logging.info(f"filename: {item['name']}")
            try:
                data = self.__download_item(item)
                records.append(
                    {
                        "id": item["id"],
                        "filename": item["name"],
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

        if any(map(lambda x: x in item["name"], ["docx", "doc"])):
            text = decode_docx(response.content)
        elif "pdf" in item["name"]:
            text = decode_pdf(response.content)
        else:
            raise Exception("Not a valid file type.")

        return text

    def __insert_records(self, records: list[dict]):
        cosmos_client.insert(records)
