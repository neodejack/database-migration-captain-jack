import pandas as pd
from pandas import DataFrame

def clean_trim_str_cols(df: DataFrame) -> DataFrame:
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    df[[
        "Name", "Contact", "Tele Handle", "Email", "Ins"
    ]] = df[[
            "Name", "Contact", "Tele Handle", "Email", "Ins"
            ]].astype(str)

    return df


def clean_tele_ins_handle(df: DataFrame) -> DataFrame:
    df["Tele Handle"] = df["Tele Handle"].apply(lambda x: x[1:] if x.startswith("@") else x)
    df["Ins"] = df["Ins"].apply(lambda x: x[1:] if x.startswith("@") else x)
    return df


def clean_convert_boolan(df: DataFrame) -> DataFrame:
    bool_map = {"p": True, "np": False}
    df["Paid or not"] = df["Paid or not"].map(bool_map)

    return df


def clean_data(df) -> DataFrame:
    df = clean_trim_str_cols(df)
    df = clean_tele_ins_handle(df)
    df = clean_convert_boolan(df)

    return df