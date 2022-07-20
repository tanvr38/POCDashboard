import json
import schedule
import os
import time
from turtle import update
import requests
import pandas as pd
import webbrowser
from datetime import date
import smtplib
import adal

# # Tenant ID for your Azure Subscription
# TENANT_ID = 'de08c407-19b9-427d-9fe8-edf254300ca7'


# # Your Service Principal App ID
# CLIENT = 'DTSS-LDPSAPIGATEWAY.B2B-STAGE'


# # Your Service Principal Password
# KEY = 'sZ8GguA9IziH8737B..VaSyqf8FJqNeR'


# subscription_id = '4d047f40-a141-4342-9700-442d3c55ffdb'

# authority_url = 'https://login.microsoftonline.com/'+TENANT_ID

# context = adal.AuthenticationContext(authority_url)

# token = context.acquire_token_with_client_credentials(
#     resource='https://management.azure.com/'
#     ,client_id=CLIENT
#     ,client_secret=KEY
# )

# print(token["accessToken"])

access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjJaUXBKM1VwYmpBWVhZR2FYRUpsOGxWMFRPSSIsImtpZCI6IjJaUXBKM1VwYmpBWVhZR2FYRUpsOGxWMFRPSSJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kZTA4YzQwNy0xOWI5LTQyN2QtOWZlOC1lZGYyNTQzMDBjYTcvIiwiaWF0IjoxNjU4MjM0NTE2LCJuYmYiOjE2NTgyMzQ1MTYsImV4cCI6MTY1ODIzOTAzMSwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhUQUFBQUxDOWtSY2VHNXdjS2JMaThJUkpxaGNjV2o1d3JNZGllUGdhMkd1V3NFLzdnK09iNUd6dGRkRmlSNTJ3TDVsR3BnV2RkSTlFMzdwR3NPMmJGOEVWdkpuaG1Nb2s5Nm02VXZDL2FyVEpQUHpVPSIsImFtciI6WyJyc2EiLCJtZmEiXSwiYXBwaWQiOiIwNGIwNzc5NS04ZGRiLTQ2MWEtYmJlZS0wMmY5ZTFiZjdiNDYiLCJhcHBpZGFjciI6IjAiLCJkZXZpY2VpZCI6IjUwMGQ0OWU1LTllOTEtNDdjNC04NDQyLTU2ZWUzODViYjZiNiIsImZhbWlseV9uYW1lIjoiTW9oZCBBa3JhbSBIYXNobWkiLCJnaXZlbl9uYW1lIjoiTW9oZCBUYW52ZWVyIiwiZ3JvdXBzIjpbIjE0MmZhNDkwLTA3YzctNDlmOS1iOGMwLTAwYTE3ZDRiNjBhOSIsImIyYjYxZTY3LTIwNDItNGIwOS04MGRmLTMzY2Q1NjdkMDVkNCIsIjkxZTM5MmJiLTkwZTItNDM3NC05MWZiLTdkOTcwNzExZmRiMCIsImMyYmEzNWFlLWNlYjMtNDQzNy04NzJmLWZmMzhiMzEwYzkwMSIsIjFlODEwY2ZhLTBhMjgtNGRmYy1hMTY5LWRjMTQ3MjdiZWM2MSIsIjE0M2JmMzRjLTk1MTUtNGY0ZC05MTIxLTk4ZmMyNzI2ODgwOCIsIjU2MTc2NDhkLTIwMDMtNGNkOC05MWQ2LTNkMzA4MzM3Mzk0ZSIsIjhiNDIwY2RiLWRhNWUtNGUwMS05Nzg5LTBlY2RhODI0MzA4MCIsIjgxZWRmOWNiLThiZDgtNDE3ZC1hNzVjLWI4Njk2MjYzZjc4ZSIsIjliMjc4OTU2LTk3MzMtNDMyZC05ZDA4LTRhYThlN2IzMmNkOCIsImM2NDY2NzQ4LTI0OTUtNDMxMC1iNDI0LTIzYmE4YjU1NWZkNiIsIjQ4YWQ2NWI0LTQzMzQtNDI4ZC1hZWYxLTRlMWQ4MjI5MjQ4ZCIsIjVjMDU2ZjdmLWUzNzktNGE2OC1hYWY1LWQzYzY0MGUyZjVjZCIsImQzYWU2MTkyLTliODAtNDU5MS1iNWUxLTJmMzYwNGY0YjVhOSIsImE2M2FlZmUzLWM5YWQtNDhmZC05MTM5LWNlYTUyNDcxMDJkZCIsIjE5M2M2ZDJjLTZkYjctNDdkZi05MzIwLTZlZWFjNWI3YTg0YiIsIjBlZDlmZTE0LTM3YWItNDdjMS05NGE4LTliYmU3ZTViMjA1ZCIsIjA5YjlkYTlhLWM1ODYtNDVkMC1hODUxLWQ4OGM0YjY2NjY2ZCIsIjU2ZGQxMjA4LTNhZTMtNGYwMC04MTNkLTUxM2RiMWZmZWQyMiIsIjZmY2UwYjU1LWUxNTAtNDgxMy1hMDJhLWU2NjU4ZmY1YjA5NCIsImQ3OWNmZDY1LWFkZmQtNDgyNy1hODBjLWNiYjMzMDhmYzM4NCIsIjc4ZTI4OTJkLTA2OGItNDc1YS1iOGU4LTkwNGE0MmY3MzNmYiIsIjQ3ZDAxOWZmLWI0MDgtNGQ5Ni1hNWZhLWIyNDZjMWY2YTk5YSIsImUxMzUyZDIyLTc2MTktNGM4OC1iZmNkLWNhNDViMzg5YjI0ZCIsImNlY2RmMGYwLTQzYTMtNDcyZi1iNDkxLTc2YTQyNzRhZTBjNiIsImE5YTlkZTIyLTJiNzEtNGY4Ny05ZTQxLWFmZmI2NmIxMTYxYyIsImM5MzY2NGE5LTQ0MWItNGI5Mi05Y2QyLWY4NzhkMzBlN2Y4MiIsImRlZmViZjUzLWNiM2YtNDQyMy05NmUyLWRmMDFmZTZlZWM0ZSIsImEyYzE2OWNlLTk0ZDctNDZhZS05OTYwLTc0OTRjODZjNjY0NiJdLCJpcGFkZHIiOiIxMDMuMjE2LjIxMi4yNiIsIm5hbWUiOiJNb2hkIEFrcmFtIEhhc2htaSwgTW9oZCBUYW52ZWVyIChDb2duaXphbnQpIiwib2lkIjoiYzE4MjRiNGEtMWE2Ni00YzVjLWFjY2UtNWNmZThmOGJkMWI0Iiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTExNzgzNjg5OTItNDAyNjc5ODA4LTM5MDQ4MjIwMC00MDI3MTQwIiwicHVpZCI6IjEwMDMyMDAxNEExMEIyMjciLCJyaCI6IjAuQVNVQUI4UUkzcmtaZlVLZjZPM3lWREFNcDBaSWYza0F1dGRQdWtQYXdmajJNQk1sQUp3LiIsInNjcCI6InVzZXJfaW1wZXJzb25hdGlvbiIsInN1YiI6IkNZbmdIS2Nsdkt1RWl6MktjMk1ZNm1tbm9XdVhwYlBBNXR1NmhuNHlub2siLCJ0aWQiOiJkZTA4YzQwNy0xOWI5LTQyN2QtOWZlOC1lZGYyNTQzMDBjYTciLCJ1bmlxdWVfbmFtZSI6Ijk0NzM1NUBjb2duaXphbnQuY29tIiwidXBuIjoiOTQ3MzU1QGNvZ25pemFudC5jb20iLCJ1dGkiOiIxaHU5aE1ZbXFrR1pSM2tYa2NZZEFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX3RjZHQiOjEzNTU4OTQ0MDl9.K3KTZ0pPp7qE64Bgf_bdgkqt6qJ4sm7-2xS4YzAOO883DuScIYduYydogqAoItiBzLiLsd777kaOKtdvaqhL7Q8e_NdnY9NJnay1yqPbaxj-ONo1LbbYhfU_ebBHNud-H4zYkfsnv9Vpj7B61rb9BWH8wJ4fMTIkqEnQCCpbtotyjZ1pm8V5wk6OFq0h0tseIqeDpvBw6VsBjHxwPtSmqS5t7uy_S18ZIRUjYK4js9s36YngsXf6QeS1nvB9HaHycPf-QFfUaK66Jn3ipqdzTf1hluVieMFckwE1Dxwd-zF5oSK_awFVESEph4BCeu7yH_Y_6Mvd2sgPGfIUml_KMA'
headers = {
  'Authorization':  'Bearer ' + access_token,
  'Content-Type': 'application/json'
}

dasboardPlot = {
    'Subscription/RG/Resource' : [],
    'Resources' : [],
    'Current Cost (INR)' : [],
    'Forecast' : [],
    'Budget (INR)' : [],
    'Threshold (%)' : [],
    'Utilization (%)' : []
}

# senderEmail = "demo.azurepoc22@gmail.com"
# senderMailPassword = "xgkuobeexsjpuyia"
# receiverEmail = ""
# emailMessage = "Hi there, this is to notify that lock has been created for Resource Group : "

# Budget & Threshold Creation taking input from an external file
inputFilePath = './input.csv'

if os.path.isfile(inputFilePath) == True :
  df = pd.read_csv('input.csv')
  for idx, row in df.iterrows():
      if idx == 0 :
          ## Budget & Threshold Creation For Subscription
          subscriptionName, subscriptionBudget, subscriptionThreshold, alertEmail = row['ResourceGroup'], row['Budget'], row['Threshold'], row['Email'].split(';')
          budgetCreationUrl = "https://management.azure.com/subscriptions/4d047f40-a141-4342-9700-442d3c55ffdb/providers/Microsoft.Consumption/budgets/TestBudget" + subscriptionName + "?api-version=2021-10-01"
          budgetCreationPayload = json.dumps({
                  "properties": {
                  "category": "Cost",
                  "amount": subscriptionBudget,
                  "timeGrain": "Monthly",
                  "timePeriod": {
                      "startDate": "2022-07-01T00:00:00Z",
                      "endDate": "2022-07-30T00:00:00Z"
                  },
                  "notifications": {
                      "Actual_GreaterThan_70_Percent": {
                      "enabled": True,
                      "operator": "GreaterThan",
                      "threshold": subscriptionThreshold,
                      "locale": "en-us",
                      "contactEmails": alertEmail,
                      "contactRoles": [],
                      "contactGroups": [],
                      "thresholdType": "Actual"
                      }
                  }
                  }
          })
          budgetCreationResponse = requests.request("PUT", budgetCreationUrl, headers=headers, data = budgetCreationPayload)
      else :
          ## Budget & Threshold Creation For Resource Groups
          resourceGroup, rsgBudget, rsgThreshold, alertEmail = row['ResourceGroup'], row['Budget'], row['Threshold'], row['Email'].split(';')
          budgetCreationUrl = "https://management.azure.com/subscriptions/4d047f40-a141-4342-9700-442d3c55ffdb/resourcegroups/" + resourceGroup + "/providers/Microsoft.Consumption/budgets/TestBudget" + resourceGroup + "?api-version=2021-10-01"
          budgetCreationPayload = json.dumps({
                  "properties": {
                  "category": "Cost",
                  "amount": rsgBudget,
                  "timeGrain": "Monthly",
                  "timePeriod": {
                      "startDate": "2022-07-01T00:00:00Z",
                      "endDate": "2022-07-30T00:00:00Z"
                  },
                  "notifications": {
                      "Actual_GreaterThan_70_Percent": {
                      "enabled": True,
                      "operator": "GreaterThan",
                      "threshold": rsgThreshold,
                      "locale": "en-us",
                      "contactEmails": alertEmail,
                      "contactRoles": [],
                      "contactGroups": [],
                      "thresholdType": "Actual"
                      }
                  }
                  }
          })
          budgetCreationResponse = requests.request("PUT", budgetCreationUrl, headers=headers, data = budgetCreationPayload)

  os.rename('input.csv', 'input_done.csv')
  print(" 'input.csv' file name has been changed to 'input_done.csv' ")

def job() :

    print("#################### START #############################")

    # fw = open('app.html', 'w')
    # fw.write('<!DOCTYPE html><head><style>thead{background-color:#3366cc;color:white}tbody{background-color:#e0e0eb;}</style></head><body>')

    lockAppliedRG = []

    getSubscriptionUrl = "https://management.azure.com/subscriptions?api-version=2020-01-01"
    getSubscriptionResponse = requests.request("GET", getSubscriptionUrl, headers=headers, data={})

    for val in getSubscriptionResponse.json()['value'] :
        subscriptionName = val['displayName']
        subscriptionId = val['subscriptionId']

        print(subscriptionName)

        ## Getting Cost of Subscription
        getSubscriptionCosturl = "https://management.azure.com/subscriptions/" + subscriptionId + "/providers/Microsoft.CostManagement/query?api-version=2021-10-01"
        getSubscriptionCostPayload = json.dumps({
            "type": "Usage",
            "timeframe": "MonthToDate",
            "dataset": {
                "granularity": "None",
                "aggregation": {
                "totalCost": {
                    "name": "PreTaxCost",
                    "function": "Sum"
                }
                }
            }
        })
        getSubscriptionCostResponse = requests.request("POST", getSubscriptionCosturl, headers=headers, data=getSubscriptionCostPayload)
        subscriptionCost = getSubscriptionCostResponse.json()['properties']['rows'][0][0]
        
        ## Getting subscription Budget and Threshold 
        getSubscriptionBudgetUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/providers/Microsoft.Consumption/budgets/" + "pocsetup" + "?api-version=2021-10-01"
        getSubscriptionBudgetResponse = requests.request("GET", getSubscriptionBudgetUrl, headers=headers, data={})

        subscriptionBudget = getSubscriptionBudgetResponse.json()['properties']['amount']
        subscriptionThreshold = getSubscriptionBudgetResponse.json()['properties']['notifications']['forecasted_GreaterThan_50_Percent']['threshold']

        subscriptionUtilization = round((subscriptionCost/subscriptionBudget)*100,2)

        ## Getting Subscription Forecast
        subscriptionForecastUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/providers/Microsoft.CostManagement/forecast?api-version=2021-10-01"
        subscriptionForecastPayload = json.dumps({
            "type": "Usage",
            "timeframe": "MonthToDate",
            "dataset": {
                "granularity": "None",
                "aggregation": {
                "totalCost": {
                    "name": "PreTaxCost",
                    "function": "Sum"
                }
                }
            }
        })
        subscriptionForecastResponse = requests.request("POST", subscriptionForecastUrl, headers=headers, data=subscriptionForecastPayload)
        subscriptionForecast = subscriptionForecastResponse.json()['properties']['rows'][0][0]
        
        
        ## Adding subscription details to dashboardPlot
        dasboardPlot['Subscription/RG/Resource'].append(subscriptionName)
        dasboardPlot['Resources'].append("Subscription Cost (Monthly)")
        dasboardPlot['Current Cost (INR)'].append(subscriptionCost)
        dasboardPlot['Forecast'].append(subscriptionForecast)
        dasboardPlot['Budget (INR)'].append(subscriptionBudget)
        dasboardPlot['Threshold (%)'].append(subscriptionThreshold)
        dasboardPlot['Utilization (%)'].append(subscriptionUtilization)




        ## Getting Subscription Yearly Cost
        subscriptionYearlyCostUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/providers/Microsoft.CostManagement/query?api-version=2021-10-01"
        subscriptionYearlyCostPayload = json.dumps({
        "type": "Usage",
        "timeframe": "Custom",
        "dataset": {
            "granularity": "None",
            "aggregation": {
            "totalCost": {
                "name": "PreTaxCost",
                "function": "Sum"
            }
            }
        },
        "timePeriod": {
            "from": "2022-01-01",
            "to": "2022-12-31"
        }
        })
        subscriptionYearlyCostResponse = requests.request("POST", subscriptionYearlyCostUrl, headers=headers, data=subscriptionYearlyCostPayload)
        subscriptionYearlyCost = subscriptionYearlyCostResponse.json()['properties']['rows'][0][0]

        ## Getting Subscription Yearly Forecast
        subscriptionYearlyForecastUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/providers/Microsoft.CostManagement/forecast?api-version=2021-10-01"
        subscriptionYearlyForecastPayload = json.dumps({
        "type": "Usage",
        "timeframe": "Custom",
        "dataset": {
            "granularity": "None",
            "aggregation": {
            "totalCost": {
                "name": "PreTaxCost",
                "function": "Sum"
            }
            }
        },
        "timePeriod": {
            "from": "2022-01-01",
            "to": "2022-12-31"
        }
        })
        subscriptionYearlyForecastResponse = requests.request("POST", subscriptionYearlyForecastUrl, headers=headers, data=subscriptionYearlyForecastPayload)
        subscriptionYearlyForecast = subscriptionYearlyForecastResponse.json()['properties']['rows'][0][0]

        ## Adding Subscription Yearly Cost & Forecast
        dasboardPlot['Subscription/RG/Resource'].append("")
        dasboardPlot['Resources'].append("Subscription Cost (Yearly)")
        dasboardPlot['Current Cost (INR)'].append(subscriptionYearlyCost)
        dasboardPlot['Forecast'].append(subscriptionYearlyForecast)
        dasboardPlot['Budget (INR)'].append("")
        dasboardPlot['Threshold (%)'].append("")
        dasboardPlot['Utilization (%)'].append("")




        ## Getting all Resource Groups in the Subscription
        getAllResourceGroupsUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourcegroups?api-version=2020-09-01"
        getAllResourceGroupsResponse = requests.request("GET", getAllResourceGroupsUrl, headers=headers, data={})

        resourceGroups = []
        resourceGroupsCosts = []
  

        for rsg in getAllResourceGroupsResponse.json()['value'] :
            resourceGroups.append(rsg['name'])

        
        for rsg in resourceGroups :

            lockAppliedRG.append(rsg)
            print(rsg)

            # dasboardPlot['Subscription/RG/Resource'].append("Resource Group")
            # dasboardPlot['Resources'].append("Resource")
            # dasboardPlot['Current Cost (INR)'].append("Current Cost (INR)")
            # dasboardPlot['Forecast'].append("Forecast")
            # dasboardPlot['Budget (INR)'].append("Budget (INR)")
            # dasboardPlot['Threshold (%)'].append("Threshold (%)")
            # dasboardPlot['Utilization (%)'].append('Utilization (%)')
            
            ## Getting all Resource Groups Costs
            rsgCostUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourcegroups/" + rsg + "/providers/Microsoft.CostManagement/query?api-version=2021-10-01"
            rsgCostPayload = json.dumps({
                "type": "Usage",
                "timeframe": "MonthToDate",
                "dataset": {
                    "granularity": "None",
                    "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                    },
                    "grouping": [
                    {
                        "type": "Dimension",
                        "name": "ResourceGroup"
                    }
                    ]
                }
            })
            rsgCostResponse = requests.request("POST", rsgCostUrl, headers=headers, data=rsgCostPayload)
            if rsgCostResponse.json()['properties']['rows'] == [] :
                resourceGroupCost = 0
            else :
                resourceGroupCost = rsgCostResponse.json()['properties']['rows'][0][0]
            

            ## Getting Budgets for all Resource Groups
            rsgBudgetUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + rsg +"/providers/Microsoft.Consumption/budgets/TestBudget" + rsg +"?api-version=2021-10-01"
            rsgBudgetResponse = requests.request("GET", rsgBudgetUrl, headers=headers, data={})
            rsgBudget = rsgBudgetResponse.json()['properties']['amount']
            rsgThreshold = rsgBudgetResponse.json()['properties']['notifications']['actual_GreaterThan_70_Percent']['threshold']
            rsgUtilization = round((resourceGroupCost/rsgBudget)*100,2)


            ## Getting Forecast For All Resource Groups
            try :
                rsgForecastUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + rsg + "/providers/Microsoft.CostManagement/forecast?api-version=2021-10-01"
                rsgForecastPayload = json.dumps({
                    "type": "Usage",
                    "timeframe": "MonthToDate",
                    "dataset": {
                        "granularity": "None",
                        "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        }
                        },
                        "includeActualCost": False,
                        "includeFreshPartialCost": False
                    }
                })
                rsgForecastResponse = requests.request("POST", rsgForecastUrl, headers=headers, data=rsgForecastPayload)
                rsgForecastCost = rsgForecastResponse.json()['properties']['rows'][0][0]

                dasboardPlot['Subscription/RG/Resource'].append(rsg)
                dasboardPlot['Resources'].append("Monthly cost")
                dasboardPlot['Current Cost (INR)'].append(resourceGroupCost)
                dasboardPlot['Forecast'].append(rsgForecastCost)
                dasboardPlot['Budget (INR)'].append(rsgBudget)
                dasboardPlot['Threshold (%)'].append(rsgThreshold)
                dasboardPlot['Utilization (%)'].append(rsgUtilization)

                # if rsgForecastCost > rsgBudget :

                #     ## Get all locks applied to the resource group
                #     rsgGetLocksUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + rsg + "/providers/Microsoft.Authorization/locks?api-version=2016-09-01"
                #     rsgGetLocksResponse = requests.request("GET", rsgGetLocksUrl, headers=headers, data={})

                #     if rsgGetLocksResponse.json()['value'] == [] :

                #         ## creating locks on RSG if "rsgForecast" > "rsgBudget"
                #         rsgLockCreationUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + rsg + "/providers/Microsoft.Authorization/locks/" + rsg + "lock?api-version=2016-09-01"
                #         rsgLockCreationPayload = json.dumps({
                #             "properties": {
                #                 "level": "ReadOnly"
                #             }
                #         })
                #         rsgLockCreationResponse = requests.request("PUT", rsgLockCreationUrl, headers=headers, data=rsgLockCreationPayload)

                #         ## Notifying User via email after creation of lock
                #         emailMessage = emailMessage + rsg 
                #         server = smtplib.SMTP('smtp.gmail.com',587)
                #         server.starttls()
                #         server.login(senderEmail,senderMailPassword)
                #         server.sendmail(senderEmail,receiverEmail,emailMessage)

            except :
                dasboardPlot['Subscription/RG/Resource'].append(rsg)
                dasboardPlot['Resources'].append("Monthly Cost")
                dasboardPlot['Current Cost (INR)'].append(resourceGroupCost)
                dasboardPlot['Forecast'].append("NA")
                dasboardPlot['Budget (INR)'].append(rsgBudget)
                dasboardPlot['Threshold (%)'].append(rsgThreshold)
                dasboardPlot['Utilization (%)'].append(rsgUtilization)


            ## Getting All Resources Cost
            try :
                rsCostUrl = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + rsg + "/providers/Microsoft.CostManagement/query?api-version=2021-10-01"
                rsCostpayload = json.dumps({
                        "type": "Usage",
                        "timeframe": "MonthToDate",
                        "dataset": {
                        "granularity": "None",
                        "aggregation": {
                            "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                            }
                        },
                        "grouping": [
                            {
                            "type": "Dimension",
                            "name": "Resourceid"
                            }
                        ]
                        }
                    })
                rsCostResponse = requests.request("POST", rsCostUrl, headers=headers, data=rsCostpayload)

                for resource in rsCostResponse.json()['properties']['rows'] :
                    resourceName = resource[1].split("/")[-1]

                    dasboardPlot['Subscription/RG/Resource'].append("")
                    dasboardPlot['Resources'].append(resourceName)
                    dasboardPlot['Current Cost (INR)'].append(resource[0])
                    dasboardPlot['Forecast'].append("")
                    dasboardPlot['Budget (INR)'].append("")
                    dasboardPlot['Threshold (%)'].append("")
                    dasboardPlot['Utilization (%)'].append("")

            except :
                dasboardPlot['Subscription/RG/Resource'].append("")
                dasboardPlot['Resources'].append("NA")
                dasboardPlot['Current Cost (INR)'].append("")
                dasboardPlot['Forecast'].append(" ")
                dasboardPlot['Budget (INR)'].append("NA")
                dasboardPlot['Threshold (%)'].append("NA")
                dasboardPlot['Utilization (%)'].append("NA")


    ## Remove Locks from RG at Day 1 of Next Month
    # if date.today().day == 1 :
    #   for rsg in lockAppliedRG :
    #     ## Get all locks applied to the resource group
    #     rsgGetLocksUrl = "https://management.azure.com/subscriptions/4d047f40-a141-4342-9700-442d3c55ffdb/resourceGroups/" + rsg + "/providers/Microsoft.Authorization/locks?api-version=2016-09-01"
    #     rsgGetLocksResponse = requests.request("GET", rsgGetLocksUrl, headers=headers, data={})
        
    #     if rsgGetLocksResponse.json()['value'] != [] :

            # for lock in rsgGetLocksResponse.json()['value'] :
            #     lockName = lock['name']
            #     deleteLockUrl = "https://management.azure.com/subscriptions/4d047f40-a141-4342-9700-442d3c55ffdb/resourceGroups/" + rsg + "/providers/Microsoft.Authorization/locks/" + lockName + "?api-version=2016-09-01"
            #     deleteLockResponse = requests.request("DELETE", deleteLockUrl, headers=headers, data={})


    
    df = pd.DataFrame(dasboardPlot)
    # df.to_csv('content.csv', index=False)
    # df = pd.read_csv('content.csv')
    # df = df.style.hide_index()
    html_view = df.style.set_table_styles([
                            {
                                "selector":"thead",
                                "props":"background-color:#3366cc; color:white;"
                            },
                            {
                                "selector":"tbody",
                                "props":"background-color:#e0e0eb;"
                            },
                        ]).hide_index().to_html()
    # df = df.set_index('Subscription/RG/Resource', inplace=True)
    # html_view = df.to_html()

    # fw.write(html_view)
    # fw.write('</body></html>')

    # htmlContent = ""

    # fr = open('app.html', 'r')
    # for line in fr.readlines() :
    #     htmlContent  += line

    # print(htmlContent)
    


    ## API for dashboard Creation
    # dashboardCreationUrl = "https://management.azure.com/subscriptions/4d047f40-a141-4342-9700-442d3c55ffdb/resourcegroups/MetlifePOC/providers/Microsoft.Resources/deployments/Test-Dashboard?api-version=2021-04-01"
    # dashboardCreationPayload = json.dumps({
    #   "properties": {
    #     "template": {
    #       "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    #       "contentVersion": "1.0.0.0",
    #       "resources": [
    #         {
    #           "type": "Microsoft.Portal/dashboards",
    #           "apiVersion": "2015-08-01-preview",
    #           "location": "centralindia",
    #           "name": "TestDashboard",
    #           "tags": {
    #             "hidden-title": "TestDashboard"
    #           },
    #           "properties": {
    #             "lenses": {
    #               "0": {
    #                 "order": 0,
    #                 "parts": {
    #                   "0": {
    #                     "position": {
    #                       "x": 0,
    #                       "y": 0,
    #                       "rowSpan": 10,
    #                       "colSpan": 13
    #                     },
    #                     "metadata": {
    #                       "inputs": [],
    #                       "type": "Extension[azure]/HubsExtension/PartType/MarkdownPart",
    #                       "settings": {
    #                         "content": {
    #                           "settings": {
    #                             "content": html_view,
    #                             "title": "Resource Groups And Resources Cost",
    #                             "subtitle": ""
    #                           }
    #                         }
    #                       }
    #                     }
    #                   }
    #                 }
    #               }
    #             }
    #           },
    #           "metadata": {}
    #         }
    #       ]
    #     },
    #     "parameters": {},
    #     "mode": "Incremental"
    #   }
    # })

    # dashboardCreationResponse = requests.request("PUT", dashboardCreationUrl, headers=headers, data=dashboardCreationPayload)


    f = open('app.html', 'w')
    f.write(html_view)
    # fw.close()
    # fr.close()

    webbrowser.open_new_tab('app.html')

    print("#################### END #############################")


job()

# schedule.every().day.at("09:00").do(job)
# schedule.every().day.at("21:00").do(job)

# while True:
#     schedule.run_pending()