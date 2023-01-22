import pandas as pd
from pandas import DataFrame
import logging
from libs.datacleaning import clean_data


def generate_sheet_df() -> DataFrame:
    df = pd.read_csv("data/member_data.csv")
    return df


def iterate_saving_all_dates(all_dates: list, df: DataFrame) -> list:
    saving_failed = []
    for date in all_dates:
        df_date = df.xs(date, axis=0, level=1, drop_level=False)

        saving_status, cid, gatewayURL = S3Controller.save_csv(date, df_date)
        db_saving_status = DbController.save_cid(date, cid, gatewayURL)

        if saving_status is False or db_saving_status is False:
            saving_failed.append(date)
            logging.info(f"date:{date} saving failure")
        logging.info(f"date:{date} saving successful")

    return saving_failed


def main():
    logging.basicConfig(filename="runtime.log",
                        level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")

    pd.set_option('display.max_columns', None)
    raw_df = generate_sheet_df()
    df = clean_data(raw_df)
    print(df.head())

    # all_dates, sheet_df = multiindex_by_date(sheet_df)
    # saving_failed = iterate_saving_all_dates(all_dates, sheet_df)


if __name__ == "__main__":
    main()
