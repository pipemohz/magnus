from decouple import config, Csv

MS_LOGIN_API = config("MS_LOGIN_API_URL", None)

MS_GRAPH_API = {
    "URL": config("MS_GRAPH_API_URL", None),
    "DRIVE_ID": config("MS_GRAPH_DRIVE_ID", None),
    "FOLDER_ID": config("MS_GRAPH_FOLDER_ID", None),
    "SCOPES": config("MS_GRAPH_SCOPES", None, cast=Csv()),
}

AZURE_APP = {
    "CLIENT_ID": config("AZ_APP_CLIENT_ID", None),
    "CLIENT_SECRET": config("AZ_APP_CLIENT_SECRET", None),
    "TENANT_ID": config("AZ_APP_TENANT_ID", None),
    "USERNAME": config("AZ_APP_USERNAME", None),
    "PASSWORD": config("AZ_APP_PASSWORD", None),
}

COSMOS = {
    "NAME": config("AZ_COSMOS_NAME"),
    "URI": config("AZ_COSMOS_URI"),
    "KEY": config("AZ_COSMOS_KEY"),
}

OPENAI = {
    "KEY": config("OPENAI_API_KEY", None),
    "MODEL": config("EMBEDDING_MODEL", "text-embedding-ada-002"),
    "ENCODING": config("EMBEDDING_ENCODING", "cl100k_base"),
    "MAX_TOKENS": config("MAX_TOKENS", 8000, cast=int),
}
