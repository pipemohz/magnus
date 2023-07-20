import logging
import azure.functions as func


from .text_search import search_text
from .embedding_text import embedding_data


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("AI function processed a request.")
    input_text = req.params.get("text")
    if not input_text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_text = req_body.get("text")

    embedding_data()
    results = search_text(input_text, n=3)

    return func.HttpResponse(results, status_code=200)
