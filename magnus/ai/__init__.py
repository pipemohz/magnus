import logging
import azure.functions as func


from .text_search import search_text


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

    results = search_text(input_text, n=3)
    output = "\n".join(results.to_list())
    return func.HttpResponse(output, status_code=200)
