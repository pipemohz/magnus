"""
Text search process
"""

# Python built-in
import logging

# FastAPI
from fastapi import HTTPException, status

# Numpy
import numpy as np

# OpenAI
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

# Pandas
import pandas as pd

# Project packages
from config.environment import OPENAI
from db import cosmos_client
from db.utils import records_to_dataframe


def search_text(input_text, n=10):
    """
    Search through the reviews for a specific product
    """
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    embedding_model = OPENAI["MODEL"]

    records = cosmos_client.get().where("IS_DEFINED(curriculums.embedding)").all()

    if not records:
        logging.info("No tokenized records.")
        return []

    df = records_to_dataframe(records)
    df.dropna(subset=["embedding"], inplace=True)

    df["embedding"] = df.embedding.apply(np.array)

    try:
        product_embedding = get_embedding(input_text, engine=embedding_model)

        df["similarity"] = df.embedding.apply(
            lambda x: cosine_similarity(x, product_embedding)
        )

        results = (
            df[["id", "web_url", "filename", "updated_at", "similarity", "abstract"]]
            .sort_values("similarity", ascending=False)
            .head(n)
        )
        results = results[results.similarity >= 0.8]
        results['abstract'] = results['abstract'].fillna("Resumen no disponible")
        # results = pd.DataFrame.to_json(results, orient="records")

    except Exception as exception:
        logging.error(f"An internal error has ocurred: {exception}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error has ocurred: {exception}",
        )
    logging.info(f"resultados: {results}")
    return results
