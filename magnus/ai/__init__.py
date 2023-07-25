import logging
import azure.functions as func
from ai.api import create_app


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("AI function processed a request.")
    app = create_app()
    return func.AsgiMiddleware(app).handle(req, context)
