# Diagrams

## Sequence diagram

This example uses a sequence diagram generated from the source below at <https://sequencediagram.org/>

```none
title Budget and contracting system integration

Contracting System->OCDS:Planning release announces\n education department intent\n to procure chairs (1)

FDP<-Finance System: Budget is allocated\n for purchase of chairs 

note over Contracting System,FDP:At this point the finance and Contracting Systems need to coordinate on the contracting process id (ocid)

Finance System-->Contracting System: Contracting system is notified of budget allocation and classification 

Contracting System-->Finance System: OR: Contracting system notifies finance system of process identifiers used to\ntake forward each budget commitment. 

Finance System->OCDS: Planning release is updated\n with confirmation of available\n budget (2)

Contracting System->OCDS: Tender is announced (3)

Contracting System->OCDS: Award is made (4)

Contracting System->OCDS: Contract is signed (4)

note over Contracting System,FDP:At this point the finance and Contracting Systems need to coordinate on the contract identifier

Contracting System-->Finance System: Make sure valid contract identifier is in finance system

Finance System->FDP: Budget is committed for 2018 

Finance System->OCDS: Contract implementation \ndetails updated with commitment\n for this year (5)

Finance System->FDP: Budget execution  for 2018 is updated

Finance System->OCDS: Contract implementation \ndetails updated with spend\n to date (6)

Finance System->FDP: Budget is committed for 2019

Finance System->OCDS: Contract implementation \ndetails updated with commitment\n for 2019 (7)

Finance System->FDP: Budget execution is updated for 2020 

Finance System->OCDS: Contract implementation \ndetails updated with commitment\n for 2020 (and modified 2019 amount) (8)

Contracting System->OCDS: Contract ends and \nfinal audit report is published (9)

Finance System->OCDS: Contract implementation \ndetails updated with final spend (10)
```

## GraphViz

Other graphics are created using GraphViz:

```shell
dot -Tpng images/figure2.dot -o images/figure2.png

dot -Tpng images/figure3.dot -o images/figure3.png
```
