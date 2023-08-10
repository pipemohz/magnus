import datetime
import logging
import asyncio
import azure.functions as func


def main(loaderTask: func.TimerRequest) -> None:
    from tasks import LoaderProcess
    from ai.embedding_text import embedding_data
    from ai.make_abstract import generate_abstract

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    if loaderTask.past_due:
        logging.info("The timer is past due!")

    logging.info("Loader task ran at %s", now)

    # Load new data from data sources
    LoaderProcess().run()
    # Tokenize records on CosmosDB by embedding_data function
    embedding_data()
    # asyncio.run(generate_abstract())

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info("Loader task finished at %s", now)
