import openai
import tiktoken

from config.environment import OPENAI
from db import cosmos_client
from db.utils import records_to_dataframe, update_records
from .requests import requests_to_openAI


def embedding_data():
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    embedding_model = OPENAI["MODEL"]
    embedding_encoding = OPENAI[
        "ENCODING"
    ]  # this the encoding for text-embedding-ada-002
    max_tokens = OPENAI["MAX_TOKENS"]  # the maximum for text-embedding-ada-002 is 8191

    # df = pd.read_csv(input_datapath, index_col=0)

    records = cosmos_client.get_embedding_empty()

    if len(records):
        df = records_to_dataframe(records)
        df.dropna(subset=["data"], inplace=True)

        encoding = tiktoken.get_encoding(embedding_encoding)

        # df = df.head(20)
        # omit reviews that are too long to embed
        df["n_tokens"] = df.data.apply(lambda x: len(encoding.encode(x)))
        df = df[df.n_tokens <= max_tokens]  # .tail(top_n)

        batch_size = 30  # 2048
        list_text = df["data"].to_list()
        segment_text = [
            list_text[i : i + batch_size] for i in range(0, len(list_text), batch_size)
        ]

        segment_embedding_text = [
            requests_to_openAI(segment, embedding_model) for segment in segment_text
        ]

        embedding_text = []
        for segment in segment_embedding_text:
            embedding_text += segment

        df["embedding"] = embedding_text

        # Apply a model to tokenized the data
        # df["embedding"] = df.data.apply(
        #     lambda x: get_embedding(x, engine=embedding_model)
        # )

        df.dropna(subset=["embedding"], inplace=True)
        if len(df):
            records = update_records(records, df)
            # print(records)
            cosmos_client.insert(records)


if __name__ == "__main__":
    embedding_data()
