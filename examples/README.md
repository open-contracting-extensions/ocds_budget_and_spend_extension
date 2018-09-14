# Examples

This section contains brief usage examples for the budgets and spend extension. Additionally, three detailed worked examples are provided:

* The **[coordination example](coordination.md)** illustrates how to express data on budget allocation and execution that may be drawn from different data systems (e.g. finance systems and procurement systems).

* The **[integration example](integration.md)** illustrates how references to a Fiscal Data Package can support display of data to users, and comparison between contracting process level and budget level data. 

* The **[flat data example](flat.md)** illustrates how the structured data published using this extension can be analysed using spreadsheet tools.

## Describing the budget line that funds a contracting process

Use the `classifications` and `measures` objects within a `planning/budget/budgetBreakdown` to provide the classifications and measures using the terminology or column headings established in an existing budget dataset. 

```json
{
  "ocid": "ocds-4f64a2-exbas-ex01",
  "planning": {
    "budget": {
      "amount": {
        "amount": 8000,
        "currency": "USD"
      },
      "budgetBreakdown": [
        {
          "id": "ED01/ED01-FAC/EQ01",
          "classifications": {
            "Dept": "ED01",
            "Economic": "Goods",
            "Func": "EQ01",
            "Team": "ED01-FAC"
          },
          "measures": {
            "Committed": 8000
          }
        }
      ]
    }
  }
}
```

Note that `Dept`, `Economic`, `Func`, `Team` and `Committed` in the example about are arbitrary keys. Any keys can be used within these objects. 

See the [integration](integration.md) example for details of how to make a link between the classifications provided here, and those used in a Fiscal Data Package dataset which provides full details of the budget. 

## Describing a contracting process funded from multiple budget lines

More than one entry in the `budgetBreakdown` array can be provided, showing how the total budget is made up of resources from a number of different budget lines. 

For example, in the case below where a contracting process is anticipated to cover the delivery of goods and the service to maintain them. 

```json
{
  "ocid": "ocds-4f64a2-exbas-ex02",
  "planning": {
    "budget": {
      "amount": {
        "amount": 8000,
        "currency": "USD"
      },
      "budgetBreakdown": [
        {
          "id": "ED01/ED01-FAC/EQ01",
          "classifications": {
            "Dept": "ED01",
            "Economic": "Goods",
            "Func": "EQ01",
            "Team": "ED01-FAC"
          },
          "measures": {
            "Committed": 5000
          }
        },
        {
          "id": "FA22/Fac/Facilities",
          "classifications": {
            "Dept": "FA22",
            "Economic": "Services",
            "Func": "Facilities",
            "Team": "Fac"
          },
          "measures": {
            "Committed": 3000
          }
        }
      ]
    }
  }
}
```

## Describing a contracting process funded from multiple sources

The `sourceParty` field provided by the [budget breakdown](https://github.com/open-contracting/ocds_budget_breakdown_extension) extension can be used, alongside, if required, different `fiscalBreakdownFieldMapping` properties. 

For example, in the extract below, we see an allocation of aid, combined with an allocation from the national budget of a country. 

```json
{
  "ocid": "ocds-4f64a2-exbas-ex03",
  "planning": {
    "budget": {
      "amount": {
        "amount": 10000,
        "currency": "USD"
      },
      "budgetBreakdown": [
        {
          "id": "01",
          "classifications": {
            "Sector": "Education",
            "Country": "Zambia",
            "Year": "2018"
          },
          "budgetBreakdown": [
            {
              "id": "01",
              "classifications": {
                "Sector":"Education",
                "Country":"Zambia",
                "Year":"2018"
              },
              "measures": {
                "Committed": 7000
              },
              "sourceParty":{
                "id":"GB-GOV-1",
                "name":"Department for International Development"
              },
              "fiscalBreakdownFieldMapping":"http://example.gov.uk/aidBudget/2018/datapackage.json#aid"
            },
            {
              "id": "FA22/Fac/Facilities",
              "classifications": {
                "Dept": "FA22",
                "Economic": "Services",
                "Func": "Facilities",
                "Team": "Fac"
              },
              "measures": {
                "Committed": 3000
              },
              "sourceParty":{
                "id":"ZM-GOV-22",
                "name":"Education Department"
              },
              "fiscalBreakdownFieldMapping":"http://example.gov.zm/nationalBudget/2018/datapackage.json#budget"
            }
          ]
        }
      ]
    }
  }
}
```


## Describing the budget to which payments have been charged

The same `breakdown` structure exists for each contract in a new `financialProgress` block. 

Through the use of `measures` indicating payment, the following extract shows a $10,000 contract which is 70% executed, where $6,000 of the execution to date is charged against a 'goods' budget line, but only $1,000 has been spent to date from the services line. 

```json
{
  "ocid": "ocds-4f64a2-exbas-ex01",
  "contracts": [
    {
      "id": "ocds-4f64a2-exbas-ex04-contract",
      "awardID": "ocds-4f64a2-exbas-ex04-award",
      "value": {
        "amount": {
          "amount": 10000,
          "currency": "USD"
        }
      },
      "financialProgress": {
        "totalSpend": {
          "amount": 7000,
          "currency": "USD"
        },
        "breakdown": [
          {
            "id": "ED01/ED01-FAC/EQ01",
            "classifications": {
              "Dept": "ED01",
              "Economic": "Goods",
              "Func": "EQ01",
              "Team": "ED01-FAC"
            },
            "measures": {
              "Paid": 6000
            }
          },
          {
            "id": "FA22/Fac/Facilities",
            "classifications": {
              "Dept": "FA22",
              "Economic": "Services",
              "Func": "Facilities",
              "Team": "Fac"
            },
            "measures": {
              "Paid": 1000
            }
          }
        ]
      }
    }
  ]
}
```

> Note: the measures used in these examples ('Committed' / 'Paid' etc.) are arbitrary keys, and any property name may be used within the `measures` object. Tools should not anticipate any specific term, and will need to refer to additional contextual information to interpret the exact fiscal measure a property relates to. 
