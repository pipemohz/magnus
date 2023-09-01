#Openai
import openai
# Python built-in
import logging
# Tiktoken
import tiktoken
# asyncio
import asyncio
# pandas
import pandas as pd

# Project packages
from config.environment import OPENAI
from db import cosmos_client
from db.utils import records_to_dataframe, add_abstract
from ai.requests import gpt_requests



async def generate_abstract():
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    model = "gpt-3.5-turbo"
    model_16k = "gpt-3.5-turbo-16k"
    encoding = OPENAI[
        "ENCODING"
    ]  # this the encoding count 
    max_tokens = 4000  # the maximum for GPT-3.5 is 4097
    creativity = 0 # this value is used to determine the creativity of the model

    records = cosmos_client.get().where("NOT IS_DEFINED(curriculums.abstract)").all()

    logging.info(f"Records without abstract: {len(records)}")

    if not records:
        logging.info("No records to make abstract.")
        return

    df = records_to_dataframe(records)
    df.dropna(subset=["data"], inplace=True)

    encoding = tiktoken.get_encoding(encoding)

    # omit reviews that are too long to embed
    df["n_tokens"] = df.data.apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens > 0]
    if not len(df):
        logging.info("No records to make abstract.")
        return

    df_16k = df[df.n_tokens > max_tokens].head(3)
    df_4k = df[df.n_tokens <= max_tokens].head(3)

    
    if len(df_4k):
        df_4k["abstract"] = await asyncio.gather(*[gpt_requests([data], model, creativity) for data in df_4k["data"]])
    if len(df_16k):
        df_16k["abstract"] = await asyncio.gather(*[gpt_requests([data], model_16k, creativity) for data in df_16k["data"]])

    df = pd.concat([df_4k, df_16k], ignore_index=True)
    # df["abstract"] = df.data.apply(lambda x: gpt_requests([x], model, creativity))


    df.dropna(subset=["abstract"], inplace=True)
    df['abstract'] = df['abstract'].astype(str)
    df = df[~df['abstract'].str.contains(r'\[nan\]', na=False)]
    if not df.empty:
        records = add_abstract(records, df)
        cosmos_client.insert(records)



