from tenacity import retry,wait_random_exponential, stop_after_attempt
from openai.embeddings_utils import get_embeddings
from openai import ChatCompletion
import numpy as np
import asyncio

def custom_retry_error_callback(retry_state):
    return [np.nan]*len(retry_state.args[0])


@retry(wait=wait_random_exponential(min=20, max=200), stop=stop_after_attempt(4), reraise=False, retry_error_callback=custom_retry_error_callback)
def requests_to_openAI(list_text: list[str], engine: str) -> list[list]:
    return get_embeddings(list_text, engine)

@retry(wait=wait_random_exponential(min=20, max=200), stop=stop_after_attempt(4), reraise=False, retry_error_callback=custom_retry_error_callback)
async def gpt_requests(data: list[str], model: str, creativity: float = 0):
    # await asyncio.sleep(200)
    response = await ChatCompletion.acreate(
        model=model,  # Puedes ajustar el motor según tus preferencias o suscripción
        messages=[
            {"role":"user", "content":fr"resumen de perfil y que idiomas habla\n\n{data[0]}"}
            ],
        temperature=creativity
    )
    return response['choices'][0]['message']['content']

# @retry(wait=wait_random_exponential(min=20, max=200), stop=stop_after_attempt(4), reraise=False, retry_error_callback=custom_retry_error_callback)
# def gpt_requests(data: list[str], model: str, creativity: float = 0):
#     response = ChatCompletion.create(
#         model=model,  # Puedes ajustar el motor según tus preferencias o suscripción
#         messages=[
#             {"role":"user", "content":fr"resumen de perfil y que idiomas habla\n\n{data[0]}"}
#             ],
#         temperature=creativity
#     )
#     return response['choices'][0]['message']['content']