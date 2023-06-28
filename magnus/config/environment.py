from decouple import config, Csv

MS_LOGIN_API = config("MS_LOGIN_API_URL", None)

MS_GRAPH_API = {
    "URL": config("MS_GRAPH_API_URL", None),
    "DRIVE_ID": config("MS_GRAPH_DRIVE_ID", None),
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
