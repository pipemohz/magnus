
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
        record["n_tokens"] = int(df.loc[df["id"] == _id, "n_tokens"].iloc[0])
        record["embedding"] = df.loc[df["id"] == _id, "embedding"].iloc[0]
    return records