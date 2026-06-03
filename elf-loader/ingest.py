import os
import json
import pandas as pd
import requests

API_KEY = os.getenv("NEW_RELIC_API_KEY")

if not API_KEY:
    raise Exception(
        "NEW_RELIC_API_KEY secret not found"
    )

df = pd.read_csv("sample-data/salesforce-elf.csv")

for _, row in df.iterrows():

    severity = (
        "HIGH"
        if row["STATUS"] == "Failure"
        else "LOW"
    )

    payload = {
        "eventType": "SalesforceELF",

        "project": "CustomerPortal",
        "environment": "TEST",
        "team": "Salesforce",
        "application": "SalesforceCRM",
        "release": "1.0",

        "severity": severity,

        "eventName": row["EVENT_TYPE"],
        "userName": row["USER_NAME"],
        "requestId": row["REQUEST_ID"],
        "executionTime": int(
            row["EXECUTION_TIME"]
        ),
        "status": row["STATUS"]
    }

    response = requests.post(
        "https://insights-collector.newrelic.com/v1/accounts/events",
        headers={
            "X-Insert-Key": API_KEY,
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )

    print(
        f"RequestId={row['REQUEST_ID']} "
        f"| Status={response.status_code}"
    )

print(
    "Salesforce ELF ingestion completed successfully."
)