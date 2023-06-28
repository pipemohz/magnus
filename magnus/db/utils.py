from pandas import DataFrame


def records_to_dataframe(
    records: list[dict], column_names: list[str] = None
) -> DataFrame:
    if column_names:
        return DataFrame.from_records(records, columns=column_names)

    return DataFrame.from_records(records)
