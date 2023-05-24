import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Formatter function processed a request.")

    return func.HttpResponse("Formatter service", status_code=200)
