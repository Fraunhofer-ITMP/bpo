<p align="center">
  <img style="width: 150px; height: 150px;" src="">
</p>

<h1 align="center">
  <br>
  <i>Bioassay Protocol Ontology (BPO)</i>
  <br>
</h1>

<p align="center">
An application ontology for extending interoperability for <i>in-vivo</i> bioassay protocols relevant to antimicrobial resistance (AMR) drug discovery.
</p>


## Why do we need it?
To enhance the reproducibility and usability of bioassays in antimicrobial resistance (AMR) associated antibacterial drug discovery and development, there is an increasing need for standardisation of bioassay metadata into machine-readable formats. Such a standardisation process requires mapping bioassay data to standard ontologies and can be performed at the study result output and protocol levels. At the result output level, general ontologies such as the BioAssay Ontology (BAO) already exist, but antibacterial drug discovery and AMR-specific ontologies that can aid in the standardisation process at the protocol level are missing. 

**Hence, we propose an application-specific ontology that will enable researchers to convert unstructured bioassay protocol data into structured machine-readable formats thereby promoting their overall reusability**.

The development of BPO is a first attempt to standardise and organise information within in-vivo AMR-related drug discovery bioassay protocol data in a structured manner. BPO will allow researchers to capture information regarding experimental details such as the type of mouse model, the bacterial strain, and the sex and growth phases of mouse and bacteria respectively from the protocol.

## Building tools

The [ROBOT](http://robot.obolibrary.org/) tool was used to build this ontology and the structure of the ontology was formulated based on the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit)

## Versioning and Formats

The ontology is available in [Ontology Web Language (OWL)](https://www.w3.org/TR/owl-guide/) format.

The **current version of the ontology is 0.0.1** and can be found [here](bpo.owl). 

BPO has officially 189 classes, only 13 are minted in the BPO namespace and probably solely because the terms requests have not been handled in a timeline compatible with your needs.

## Ontology Overview

Since the current ontology is an application ontology, it makes use of various existing ontologies for its purpose. The ontologies used, and the number of terms extracted from them are shown below:

[comment]: <> (| Ontology Name | Ontology abbreviation | Number of terms |)

[comment]: <> (| --------------- | --------------- | --------------- |)

[comment]: <> (| Row 1 Column 1 | NCBITaxon | Row 1 Column 3 |)

[comment]: <> (| Row 2 Column 1 | PATO | Row 2 Column 3 |)

[comment]: <> (| Row 3 Column 1 | Row 3 Column 2 | Row 3 Column 3 |)

## Developers / Contributors
| Person | Role |
| --- | ----------- |
| [Yojana Gadiya](https://orcid.org/0000-0002-7683-0452) | Maintainers and Developer |
| [Rakel Arrazuria](https://orcid.org/0000-0002-0757-3915) | Domain expert | 
| [Jon Ulf Hansen](https://orcid.org/0000-0002-6410-5755) | Domain expert | 
| [Danielle Welter](https://orcid.org/0000-0003-1058-2668) | Ontology expert | 
| [Fuqi Xu](https://orcid.org/0000-0002-5923-3859) | Co-developer and ontology expert | 
| [Philippe Rocca-Serra](https://orcid.org/0000-0001-9853-5668) | Ontology expert | 
| [Nick Juty](https://orcid.org/0000-0002-2036-8350) | Project Lead | 
| [Philip Gribbon](https://orcid.org/0000-0001-7655-2459) | Project Lead |


## Affiliations and Funders
This research was funded by the EU/EFPIA Innovative Medicines Initiative 2 Joint Undertaking project Collaboration for prevention and treatment of MDR bacterial infections ([COMBINE](https://amr-accelerator.eu/project/combine/)) IMI2 JU (grant agreement # 853967) and [FAIRplus](https://www.imi.europa.eu/projects-results/project-factsheets/fairplus) (grant agreement # 802750).

![IMI](images/logo/affiliation-logo.png)
