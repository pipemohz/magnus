import logging
import pandas as pd
import numpy as np
import openai
import os


from ast import literal_eval
from openai.embeddings_utils import get_embedding, cosine_similarity
from config.environment import OPENAI
from db import cosmos_client
from db.utils import records_to_dataframe

from fastapi import HTTPException, status


# search through the reviews for a specific product
def search_text(input_text, n=10):
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    embedding_model = OPENAI["MODEL"]

    records = cosmos_client.get_records_with_embedding()

    if not records:
        return records

    df = records_to_dataframe(records)
    df.dropna(subset=["embedding"], inplace=True)

    df["embedding"] = df.embedding.apply(np.array)

    try:
        product_embedding = get_embedding(input_text, engine=embedding_model)

        df["similarity"] = df.embedding.apply(
            lambda x: cosine_similarity(x, product_embedding)
        )

        results = (
            df[["id", "web_url", "updated_at", "similarity"]]
            .sort_values("similarity", ascending=False)
            .head(n)
        )
        results = pd.DataFrame.to_json(results, orient="records")

    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error has ocurred: {exception}",
        )

    return results
