import datetime
import logging

import azure.functions as func


def main(loaderTask: func.TimerRequest) -> None:
    from tasks import LoaderProcess

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    if loaderTask.past_due:
        logging.info("The timer is past due!")

    logging.info("Loader task ran at %s", now)

    LoaderProcess().run()

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info("Loader task finished at %s", now)
