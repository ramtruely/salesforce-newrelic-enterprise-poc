import os
import json
import pandas as pd
import requests

API_KEY = os.getenv("NEW_RELIC_API_KEY")

if not API_KEY:
    raise Exception(
        "NEW_RELIC_API_KEY secret not found"
    )

df = pd.read_csv(
    "sample-data/salesforce-exceptions.csv"
)

for _, row in df.iterrows():

    payload = {
        "eventType": "SalesforceException",

        "project": "CustomerPortal",
        "environment": "TEST",
        "team": "Salesforce",
        "application": "SalesforceCRM",

        "className": row["CLASS_NAME"],
        "exceptionType": row["EXCEPTION_TYPE"],
        "severity": row["SEVERITY"],
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
        f"{row['EXCEPTION_TYPE']} "
        f"| Status={response.status_code}"
    )

print(
    "Salesforce Exception ingestion completed successfully."
)