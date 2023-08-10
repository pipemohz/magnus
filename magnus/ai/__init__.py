import logging
import azure.functions as func
from ai.api import create_app
from ai.make_abstract import generate_abstract


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("AI function processed a request.")
    return func.AsgiMiddleware(create_app()).handle(req, context)
