[comment]: <> (<p align="center">)

[comment]: <> (  <img style="width: 150px; height: 150px;" src="">)

[comment]: <> (</p>)

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

The ontology is available in [Ontology Web Language (OWL)](https://www.w3.org/TR/owl-guide/) and [Open Biomedical Ontologies (OBO)](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html)format.

The **latest version of the ontology is 0.0.1** and can be found [here]([bpo_0.0.1.owl](https://github.com/Fraunhofer-ITMP/bpo/tree/main/release/v0.0.1)). 

BPO has 209 classes and 2,242 axioms and follows the BFO top-level ontology tree.

## Ontology Overview

Since the current ontology is an application ontology, it makes use of various existing ontologies for its purpose. The ontologies used, and the number of terms extracted from them are shown below:

| Ontology Name | Ontology abbreviation | Number of terms | BFO compliant |
| --------------- | --------------- | --------------- | --------------- |
| NCBI taxonomy database| NCBITaxon | 120 | No |
| Phenotype And Trait Ontology | PATO | 7 | Yes |
| National Cancer Institute Thesaurus | NCIt | 13 | No |
| Vaccine Ontology | VO | 1 | No |
| Ontology for Biomedical Investigations | OBI | 4 | Yes |
| Ontology for MIRNA Target | OMIT | 1 | Yes |
| Microbial Conditions Ontology | MCO | 3 | Yes |
| Infectious Disease Ontology | IDO | 3 | Yes |
| Experimental Factor Ontology | EFO | 7 | Yes |
| *Bioassay Protocol Ontology* | BPO | 32 | Yes |

To get a brief overview of the project, check out the **ESCMID 2022 Conference Poster** below:
<object data="images/ESCMID - BPO Poster.pdf" width="800" height="500"></object>

## Developers / Contributors

<table>
  <tr>
    <th>Person Name</th>
    <th>Affiliation</th>
    <th>Role</th>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0002-7683-0452'>Yojana Gadiya</a></td>
    <td>Fraunhofer Insititue for Translational and Medicine Pharamcology</td>
    <td>Maintainer and Developer</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0002-0757-3915'>Rakel Arrazuria</a></td>
    <td>Paul-Ehrlich-Institut</td>
    <td>Domain expert</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0002-6410-5755'>Jon Ulf Hansen</a></td>
    <td>Statens Serum Institut</td>
    <td>Domain expert</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0003-1058-2668'>Danielle Welter</a></td>
    <td>Luxembourg Centre for Systems Biomedicine</td>
    <td>Ontology expert</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0002-5923-3859'>Fuqi Xu</a></td>
    <td>European Molecular Biology Laboratory</td>
    <td>Co-developer and ontology expert</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0001-9853-5668'>Philippe Rocca-Serra</a></td>
    <td>University of Oxford e-Research Centre</td>
    <td>Ontology expert</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0002-2036-8350'>Nick Juty</a></td>
    <td>University of Manchester</td>
    <td>Project Lead</td>
  </tr>
  <tr>
    <td><a href='https://orcid.org/0000-0001-7655-2459'>Philip Gribbon</a></td>
    <td>Fraunhofer Insititue for Translational and Medicine Pharamcology</td>
    <td>Project Lead</td>
  </tr>
</table>


## Affiliations and Funders
This research was funded by the EU/EFPIA Innovative Medicines Initiative 2 Joint Undertaking project Collaboration for prevention and treatment of MDR bacterial infections ([COMBINE](https://amr-accelerator.eu/project/combine/)) IMI2 JU (grant agreement # 853967) and [FAIRplus](https://www.imi.europa.eu/projects-results/project-factsheets/fairplus) (grant agreement # 802750).

![IMI](images/logo/affiliation-logo.png)
