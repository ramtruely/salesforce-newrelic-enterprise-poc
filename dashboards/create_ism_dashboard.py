import os
import requests
import json

API_KEY = os.getenv("NEW_RELIC_USER_API_KEY")
ACCOUNT_ID = int(os.getenv("NEW_RELIC_ACCOUNT_ID"))

url = "https://api.newrelic.com/graphql"

query = """
mutation CreateDashboard($accountId: Int!) {
  dashboardCreate(
    accountId: $accountId,
    dashboard: {
      name: "ISM Dashboard"
      permissions: PUBLIC_READ_WRITE

      pages: [
        {
          name: "Platform Health"

          widgets: [

            {
              title: "Total Platform Events"
              visualization: BILLBOARD

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT count(*) FROM SalesforceELF"
                  }
                ]
              }
            }

            {
              title: "Success Rate"
              visualization: BILLBOARD

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT percentage(count(*), WHERE status='Success') FROM SalesforceELF"
                  }
                ]
              }
            }

            {
              title: "Failure Trend"
              visualization: LINE

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT count(*) FROM SalesforceELF WHERE status='Failure' TIMESERIES"
                  }
                ]
              }
            }

          ]
        }
      ]
    }
  ) {
    entityResult {
      guid
      name
    }
  }
}
""" % (ACCOUNT_ID, ACCOUNT_ID, ACCOUNT_ID)

response = requests.post(
    url,
    headers={
        "API-Key": API_KEY,
        "Content-Type": "application/json"
    },
    json={
        "query": query,
        "variables": {
            "accountId": ACCOUNT_ID
        }
    }
)

print(response.status_code)
print(json.dumps(response.json(), indent=2))