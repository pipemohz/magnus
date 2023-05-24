import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("AI function processed a request.")

    return func.HttpResponse("AI service", status_code=200)
