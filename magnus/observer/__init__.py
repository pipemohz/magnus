import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Observer function processed a request.")

    return func.HttpResponse("Observer service", status_code=200)
