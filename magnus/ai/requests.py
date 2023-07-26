from tenacity import retry,wait_random_exponential, stop_after_attempt
from openai.embeddings_utils import get_embeddings
import numpy as np

def custom_retry_error_callback(retry_state):
    return [np.nan]*len(retry_state.args[0])

@retry(wait=wait_random_exponential(min=20, max=200), stop=stop_after_attempt(4), reraise=False, retry_error_callback=custom_retry_error_callback)
def requests_to_openAI(list_text: list[str], engine: str) -> list[list]:
    return get_embeddings(list_text, engine)