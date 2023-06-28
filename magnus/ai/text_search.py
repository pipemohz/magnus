import pandas as pd
import numpy as np
import openai
import os


from openai.embeddings_utils import get_embedding, cosine_similarity
from dotenv import load_dotenv


# search through the reviews for a specific product
def search_text(input_text, n=3, pprint=True):
    load_dotenv("ai/config.env")
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # embedding model parameters
    embedding_model = os.environ.get("EMBEDDING_MODEL")

    datafile_path = "ai/data/fine_food_reviews_with_embeddings_1k.csv"

    df = pd.read_csv(datafile_path)
    df["embedding"] = df.embedding.apply(eval).apply(np.array)
    product_embedding = get_embedding(input_text, engine=embedding_model)

    df["similarity"] = df.embedding.apply(
        lambda x: cosine_similarity(x, product_embedding)
    )

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
        .combined.str.replace("Title: ", "")
        .str.replace("; Content:", ": ")
    )
    matchs = df.sort_values("similarity", ascending=False).head(n)
    print(matchs.combined)
    if pprint:
        for r in results:
            print(r[:400])
            print()
    return results


# results = search_text(df, "delicious beans", n=3)
# print(results)
