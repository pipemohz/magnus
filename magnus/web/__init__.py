import logging

import azure.functions as func
from web.app import create_app


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    app = create_app()
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
