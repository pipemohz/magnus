
from typing import Dict
import pandas
from pandas import DataFrame


def records_to_dataframe(
    records: list[dict], column_names: list[str] = None
) -> DataFrame:
    if column_names:
        return DataFrame.from_records(records, columns=column_names)

    return DataFrame.from_records(records)

def update_records(
    records: list[Dict[str, any]], df: pandas.DataFrame
) -> list[Dict[str, any]]:

    for record in records:
        _id = record["id"]
        serie = df[["n_tokens", "embedding"]][df["id"]==_id]
        if len(serie):
            record["n_tokens"] = int(serie.iloc[0, 0])
            record["embedding"] = serie.iloc[0, 1]
    return records