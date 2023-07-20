import pandas as pd
import tiktoken
import openai
import os
import json


from config.environment import OPENAI
from db import cosmos_client
from db.utils import records_to_dataframe, update_records
from openai.embeddings_utils import get_embedding


def embedding_data():
    
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    embedding_model = OPENAI["MODEL"]
    embedding_encoding = OPENAI["ENCODING"] # this the encoding for text-embedding-ada-002
    max_tokens = OPENAI["MAX_TOKENS"]  # the maximum for text-embedding-ada-002 is 8191
    
    # df = pd.read_csv(input_datapath, index_col=0)

    records = cosmos_client.get_embedding_empty("curriculums")
    
    if len(records):
        df = records_to_dataframe(records)
        df.dropna(subset=["data"], inplace=True)

        encoding = tiktoken.get_encoding(embedding_encoding)

        # omit reviews that are too long to embed
        df["n_tokens"] = df.data.apply(lambda x: len(encoding.encode(x)))
        df = df[df.n_tokens <= max_tokens] #.tail(top_n)

        # Apply a model to tokenized the data
        df["embedding"] = df.data.apply(
            lambda x: get_embedding(x, engine=embedding_model)
        )

        records = update_records(records, df)

        cosmos_client.insert("curriculums", records)


if __name__ == "__main__":
    embedding_data()
