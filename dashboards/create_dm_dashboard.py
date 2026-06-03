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
      name: "DM Dashboard"
      permissions: PUBLIC_READ_WRITE

      pages: [
        {
          name: "Delivery Overview"

          widgets: [

            {
              title: "Project Health"
              visualization: PIE

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT count(*) FROM SalesforceELF FACET project"
                  }
                ]
              }
            }

            {
              title: "Release Distribution"
              visualization: BAR

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT count(*) FROM SalesforceELF FACET release"
                  }
                ]
              }
            }

            {
              title: "Risk Distribution"
              visualization: PIE

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT count(*) FROM SalesforceException FACET severity"
                  }
                ]
              }
            }

            {
              title: "Top Exceptions"
              visualization: TABLE

              rawConfiguration: {
                nrqlQueries: [
                  {
                    accountId: %d
                    query: "SELECT count(*) FROM SalesforceException FACET exceptionType"
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
""" % (
    ACCOUNT_ID,
    ACCOUNT_ID,
    ACCOUNT_ID,
    ACCOUNT_ID
)

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