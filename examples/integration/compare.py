"""
This file is part of a worked example to show how OCDS data can be compared to
data published using the Fiscal Data Package.

In this example, we take a number of shortcuts: preparing a flat version of
our OCDS data, and reading the underlying FDP tables directly.

A full implementation would:

* Read OCDS data directly
* Use datapackage.json to understand the logical model of an FDP file
"""

import pandas as pd

fdp = pd.read_csv("fdp/budget-and-spend.csv")
ocds = pd.read_csv("financialProgress-extract.csv")

merged = pd.merge(
    ocds,
    fdp,
    how="left",
    left_on=[
        "classifications/Year",
        "classifications/Dept",
        "classifications/Economic",
        "classifications/Team",
        "classifications/Func",
    ],
    right_on=[
        "Year",
        "Dept",
        "Economic",
        "Team",
        "Func",
    ],
)

merged.to_csv("budget-contracting-compared.csv", index=False)
