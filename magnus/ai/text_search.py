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
from ai.requests import requests_to_openAI
from config.environment import OPENAI
from db.utils import records_to_dataframe


def search_text(input_text, records, n=10, similarity=0.8):
    """
    Search a profile using cosine similarity
    """
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    embedding_model = OPENAI["MODEL"]

    if not records:
        logging.info("No tokenized records.")
        return []

    df = records_to_dataframe(records)
    df.dropna(subset=["embedding"], inplace=True)

    df["embedding"] = df.embedding.apply(np.array)

    if not "abstract" in df.columns:
        df["abstract"] = np.nan

    try:
        product_embedding = get_embedding(input_text, engine=embedding_model)

        df["similarity"] = df.embedding.apply(
            lambda x: cosine_similarity(x, product_embedding)
        )

        if n == -1:
            n = len(df)

        results = (
            df[["id", "web_url", "filename", "updated_at", "similarity", "abstract"]]
            .sort_values("similarity", ascending=False)
            .head(n)
        )
        results = results[results.similarity >= similarity]
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


def search_keywords(input_keywords: list[str], records):
    """
    Filter a profile using keywords with cosine similarity
    """
    openai.api_key = OPENAI["KEY"]

    # embedding model parameters
    embedding_model = OPENAI["MODEL"]

    if not records:
        logging.info("No tokenized records.")
        return []

    df = records_to_dataframe(records)
    df.dropna(subset=["embedding"], inplace=True)

    df["embedding"] = df.embedding.apply(np.array)
    pre_filter = np.zeros(len(df.embedding))
    try:
        embedding_keywords = requests_to_openAI(input_keywords, embedding_model)
        for keyword in embedding_keywords:

            df["similarity"] = df.embedding.apply(
                lambda x: cosine_similarity(x, keyword)/len(embedding_keywords)
            )
            pre_filter += df["similarity"]

        if isinstance(pre_filter, pd.Series):
            results = df[["id", "similarity"]]
            results["similarity"] = pre_filter/100
            return results
        else:
            return None

    except Exception as exception:
        logging.error(f"An internal error has ocurred: {exception}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error has ocurred: {exception}",
        )
    