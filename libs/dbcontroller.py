import io
import os
import requests

import boto3
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

load_dotenv()


class DbController:
    db = boto3.resource("dynamodb",
                          region_name=os.getenv("AWS_DEFAULT_REGION"),
                          aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                          )

    table = db.Table(os.getenv("TRIAGE_DATA_MIGRATION_TABLE"))

    @classmethod
    def save_cid(cls, date: str, cid: str, gatewayURL: str) -> bool:
        dynamodb_res = DbController.table.put_item(
            Item={
                "date": date,
                "cid": cid,
                "gatewayURL": gatewayURL,
            }
        )
        status = dynamodb_res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status != 200:
            return False
        return True
