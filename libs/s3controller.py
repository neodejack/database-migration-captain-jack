import io
import os
from typing import Tuple
import requests

import boto3
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

load_dotenv()


class S3Controller:
    s3 = boto3.resource("s3")
    bucket = os.getenv("S3_BUCKET")
    web3_storage_api_url = os.getenv("WEB3_STORAGE_API_URL")

    @classmethod
    def save_csv(cls, date_unformatted: str, df: DataFrame) -> Tuple[bool, str, str]:
        try:
            date = date_unformatted.replace("/", "-")
        except AttributeError:
            pass
        file_name = f"sev-legacy-tickets/{date}.csv"
        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=True)
            # store csv in s3
            s3_object = S3Controller.s3.Object(S3Controller.bucket, file_name)
            s3_response = s3_object.put(
                Body=csv_buffer.getvalue()
            )
            # store csv in web3.storage
        csv_output = df.to_csv()
        files = {
            "file": (f"{date}.csv", csv_output)
        }

        web3_res = requests.post(f"{S3Controller.web3_storage_api_url}/store_dev", files=files)
        status = s3_response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status != 200 or web3_res.status_code != 200:
            return False, "error", "error"
        res_json = web3_res.json()
        cid = res_json["cid"]
        gatewayURL = res_json["gatewayURL"]
        return True, cid, gatewayURL
