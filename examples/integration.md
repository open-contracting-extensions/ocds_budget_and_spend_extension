# Integration with Fiscal Data Package

This worked example shows how the `fiscalBreakdownFieldMapping` field can be used to:

* (a) Provide labels and annotations for each of the `classifications` and `measures` in an OCDS `budgetBreakdown` or `implementation/financialProgress/breakdown` section.

* (b) Show the connection between budget allocated to a particular contracting process, and higher-level budget allocations.

## Prose description

The Department of Education have a budget of USD 20,000 for the purchase of equipment each year. They identify the need for chairs for schools, and start a procurement for this. They initially use contracts in which they purchase the chairs direct, but over time, shift to use of contracts for providers to rent chairs to them as part of a wider package of managed facilities.

The government create a website that will show:

* The budget source(s) of the procurement;
* A link to see how this budget source fits into the wider government budget;
* Details of how far executed the budget is;
* A link to details of wider budget execution. 

## Components

### Budget and spending dataset

In this example we use a very simple budget file for the Department for Education, in which they allocate resources between 'Equipment' (i.e. buying chairs and tables) and 'Managed services' (i.e. paying for a company to provide chairs and tables on a rental basis). 

| Year | Dept | DeptName  | Team     | TeamName      | Economic | Func | FuncDesc    | Committed | Modified | Paid  | 
|------|------|-----------|----------|----------------------|----------|------|--------------------|-----------|----------|-------| 
| 2015 | ED01 | Education | ED01-FAC | Education Facilities | Services | SE01 | Managed facilities | 2000      | 2000     | 3000  | 
| 2015 | ED01 | Education | ED01-FAC | Education Facilities | Goods    | EQ01 | Equipment   | 20000     | 20000    | 15000 | 
| 2016 | ED01 | Education | ED01-FAC | Education Facilities | Services | SE01 | Managed facilities | 5000      | 5000     | 6000  | 
| 2016 | ED01 | Education | ED01-FAC | Education Facilities | Goods    | EQ01 | Equipment   | 18000     | 18000    | 18000 | 
| 2017 | ED01 | Education | ED01-FAC | Education Facilities | Services | SE01 | Managed facilities | 10000     | 10000    | 11000 | 
| 2017 | ED01 | Education | ED01-FAC | Education Facilities | Goods    | EQ01 | Equipment   | 10000     | 10000    | 18000 | 

In this example, the information is maintained in a single government wide budget dataset ([budget-and-spend.csv](integration/fdp/budget-and-spend.csv)) which is updated regularly. The extract from this above shows that in 2015, more money was allocated to buying equipment directly, with some minor planned and executed spend on managed facilities. By 2017, more an equal amount is being spent on managed facilities, and on directly purchased equipment.

The columns in this budget file are described by a Fiscal Data Package [datapackage.json](integration/fdp/datapackage.json) file which contains a schema for [budget-and-spend.csv](integration/fdp/budget-and-spend.csv) as shown in the extract below:

*Extract from [datapackage.json](integration/fdp/datapackage.json)*

```
{
"resources": [
    {
      "name": "budget-and-spend",
      "path": "budget-and-spend.csv",
      "profile": "tabular-data-resource",
      "schema": {
 "fields": [
   {
     "name": "Year",
     "type": "date",
     "format": "default",
     "title": "Year",
     "description": "Financial year",
     "columnType": "date:fiscal-year"
   },
   {
     "name": "Dept",
     "type": "string",
     "format": "default",
     "title": "Department Code",
     "columnType": "administrative-classification:generic:level1:code"
   },
   {
     "...":"..."
   }
      }
  }
}
```

This contains a `name` field which matches a column from [budget-and-spend.csv](integration/fdp/budget-and-spend.csv), as well as a `label`, and `columnType` for each column. The Fiscal Data Package defines a number of other possible properties, including properties that indicate when one column is `labelOf` another, or when columns should be considered ordered, using a `prior` property. 

> Note: In practice, this data might be split across data files by year, and in separate files for budget and spend. Or it may be provided through an API. The coordination example shows how each `budgetBreakdown` or `implementation/financialProgress/breakdown` can make use of a different `fiscalBreakdownFieldMapping` file if required. 

### Contracting dataset

Contracting information is expressed using a set of OCDS releases. The [coordination](coordination.md) example shows how data can be built up over time through a series of releases. In this example, we show just one compiled release from the end of 2017, showing information to date on the contracting processes for the purchase of chairs for a specific school. In the example, two contracts are awarded from this single process, resulting in two contracts, each with a different supplier. A similar process might also exist for the procurement of managed services, although this is not illustrated in the example at present. 

The [OCDS file](integration/ocds-4f64a2-exbas-integration.json) shows the compiled release that contains both a `planning/budget/budgetBreakdown` section showing the budget committed from a budget line **for this particular contracting process**, and `contracts/implementation/financialProgress/breakdown` section showing the amount paid from a budget line, again for this specific contracting process.

Each extended breakdown entry contains a `fiscalBreakdownFieldMapping` field pointing to the relevant [datapackage.json](integration/fdp/datapackage.json), and using a fragment identifier (#) to point to the particular resource inside that file that describes each of the classifications and measures, and the budget level data file that the contacting level measures can be compared to. 

*Extract of [OCDS compiled release](integration/ocds-4f64a2-exbas-integration.json) showing `contracts/implementation/financialProgress/breakdown` section*.

```
{
  "classifications": {
    "Dept": "ED01",
    "Economic": "Goods",
    "Func": "EQ01",
    "Team": "ED01-FAC",
    "Year": "2017"
  },
  "id": "2017/ED01/ED01-FAC/EQ01",
  "measures": {
    "Paid": 950
  },
  "period": {
    "startDate": "2017-01-01T00:00:00Z",
    "endDate": "2017-12-31T23:23:59Z"
  },
  "fiscalBreakdownFieldMapping": "https://raw.githubusercontent.com/ocds_budget_and_spend_extension/master/examples/integration/fdp/datapackage.json#budget-and-spend"
}
```

## Integration in action

### Labelling fields

Using the OCDS data alone, an interface wishing to display budget classification would only have access to the key-value pairs in the `classifications` object. For example, presenting fields as below:

| Dept | Economic | Func | Team | Year |
|------|----------|------|------|------|
| ED01 | Goods    | EQ01 | ED01-FAC | 2017 |

However, by using the field titles and meta-data provided in the [datapackage.json](integration/fdp/datapackage.json) file, an interface is able to provide more user friendly labels, such as:

| Department | Economic Classification | Functional Classification | Team | Year |
|------|----------|------|------|------|
| ED01 | Goods    | EQ01 | ED01-FAC | 2017 |

A suitably sophisticated tool could go further, using the `columnType` data from the [datapackage.json](integration/fdp/datapackage.json) file to format dates and classifications appropriately, to order the display of fields, and to extract labels for codes, such as:

| Year | Department | Team |  Economic Classification | Functional Classification | 
|------|----------|------|------|------|
| FY17 | Education | Education Facilities | Goods | Equipment |  

### Making links

Where the systems used to publish OCDS data and Budget/Spending data for public consumption provide RESTFul URI structures then it may be possible to construct links that help users navigate between budget, contracting and spend systems.

For example: 

* a budget system may support querystring parameters for each classification in order to filter the information it displays, such that a URI could be constructed that links from contracting data to the budget information.

> E.g. http://budget.example.gov/details?Year=2017&Economic=Goods&Func=EQ01&Team=ED01-FAC&Dept=ED01

* a contracting system may provide an API that will return all budget or financialProgress related to a particular combination of budget classifications, such that the budget system can list contracts related to a given budget line. 

### Comparing data

The OCDS release shows the budget allocations and executions **at the level of a single contracting process and for each contract**. 

In this example, the Fiscal Data Package contains budget data at the level of broad budget classifications, and *not* at the level of individual contracting processes or contract.

To understand how much of the total budget line the contracts in our example make up, we can use the `classifications` information to cross-reference the budget data. 

> Note: depending on how a Fiscal Data Package is implemented, this cross-reference may be possible against the underlying data file (budget-and-spend.csv), or may only be possible against some API (such as the Open Spending API) where any normalisation described by the datapackage.json file has already been carried out. When querying normalised data, it may be necessary to check how measure fields have been normalised in order to construct an appropriate API call. 
>
> This extension does not define the exact behaviour of any API or FDP dataset, and each implementation may need to accommodate cases where a query returns multiple budget lines.

In our simplified example, comparing budgets would show:

| Year | Contracting process budget | Total of budget line | %age contracting process of budget |
|------|----------------------------|----------------------|-------|
| 2015 | 5000 | 20000 | 25% |
| 2016 | 3000 | 18000 | 16.6% | 
| 2017 | 1000 | 10000 | 10% | 

At the contract level, we can then generate the following summary:

| Contract ID  | Supplier    | Year | Contract amount paid | Budget line execution total | %age of budget taken by contract | 
|---------------------|-------------|------|----------------------|-----------------------------|----------------------------------| 
| ocds-...-contract-1 | AnyCorp Ltd | 2015 | 3000  | 15000 | 20.0%      | 
| ocds-...-contract-1 | AnyCorp Ltd | 2016 | 1000  | 18000 | 5.6%| 
| ocds-...-contract-1 | AnyCorp Ltd | 2017 | 950   | 18000 | 5.3%| 
| ocds-...-contract-2 | Chair Co    | 2015 | 50    | 15000 | 0.3%| 
| ocds-...-contract-2 | Chair Co    | 2016 | 1000  | 18000 | 5.6%| 
| ocds-...-contract-2 | Chair Co    | 2017 | 1600  | 18000 | 8.9%| 

This shows how, over time, the share of the budget allocated to particular suppliers has shifted. 

