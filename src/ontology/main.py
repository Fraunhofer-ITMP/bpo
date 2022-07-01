# -*- coding: utf-8 -*-

"""File to create th BPO ontology."""

import logging
import os

ONTOLOGY_IMPORT_DIR = 'imports'
LIB_DIR = '../../bin'
ONTOLOGY_EXPORT_DIR = '../../imports'
TEMPLATE_DIR = '../templates'

logger = logging.getLogger(__name__)


def get_robot(
    install_latest: bool = False
):
    """Get latest version of ROBOT.

    @param install_latest: Whether to install the latest version of ROBOT or not.
    """
    os.makedirs(LIB_DIR, exist_ok=True)

    if not install_latest:
        return

    # Get latest ROBOT jar file:
    get_robot_curl = f"curl -L https://build.obolibrary.io/job/ontodev/job/robot/job/master/lastSuccessfulBuild" \
                     f"/artifact/bin/robot.jar > {LIB_DIR}/robot.jar "
    try:
        os.system(get_robot_curl)
    except IOError as ioe_curl:
        print(ioe_curl)

    return logger.warning('Successfully installed the latest version of ROBOT. \n')


def get_full_ontology(
    onto_uri: str,
    onto_name: str
):
    """Get OWL files for existing ontology to re-use in your current ontology.

    :param onto_uri: PURL URI of the ontology.
    :param onto_name: The file name of the ontology to be stored with the OWL extension.
    """

    logger.warning(f'Getting {onto_uri} ontology')

    try:
        os.system(f"curl -L {onto_uri}  > {ONTOLOGY_IMPORT_DIR}/{onto_name}")
    except IOError as ioe_curl:
        print(ioe_curl)

    logger.warning(f'Ontologies downloaded successfully :) \n')


def main():
    """Workflow to create the BPO ontology."""

    get_robot()

    """Download all base ontologies"""
    # NCIT tree
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/ncit.owl'):
        get_full_ontology(
            onto_uri='http://purl.obolibrary.org/obo/ncit.owl',
            onto_name='ncit.owl'
        )

    # NCBITaxon
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/ncbitaxon.owl'):
        get_full_ontology(
            onto_uri='http://purl.obolibrary.org/obo/ncbitaxon.owl',
            onto_name='ncbitaxon.owl'
        )

    # EFO
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/efo.owl'):
        get_full_ontology(
            onto_uri=' http://www.ebi.ac.uk/efo/efo.owl',
            onto_name='efo.owl'
        )

    # PATO
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/pato.owl'):
        get_full_ontology(
            onto_uri='http://purl.obolibrary.org/obo/pato.owl',
            onto_name='pato.owl'
        )

    # MCO
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/mco.owl'):
        get_full_ontology(
            onto_uri='http://purl.obolibrary.org/obo/mco.owl',
            onto_name='mco.owl'
        )

    # IDO
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/ido.owl'):
        get_full_ontology(
            onto_uri='http://purl.obolibrary.org/obo/ido.owl',
            onto_name='ido.owl'
        )

    # BFO
    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/bfo.owl'):
        get_full_ontology(
            onto_uri='http://purl.obolibrary.org/obo/bfo.owl',
            onto_name='bfo.owl'
        )

    """Trimming the NCIT"""

    logger.warning(f'Refactoring NCIT')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar extract --method STAR -i {ONTOLOGY_IMPORT_DIR}/ncit.owl \
            --term-file {ONTOLOGY_IMPORT_DIR}/ncit_terms.txt --copy-ontology-annotations true --intermediates all \
            --imports exclude -o {ONTOLOGY_EXPORT_DIR}/ncit_extracted.owl"
    )

    # Refactoring the NCIT ontology to BFO format using VO tree
    os.system(
        f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_EXPORT_DIR}/ncit_extracted.owl \
            --template {TEMPLATE_DIR}/ncit_vo_tree.tsv merge -i {ONTOLOGY_EXPORT_DIR}/ncit_extracted.owl \
            --include-annotations true reduce --reasoner ELK -o {ONTOLOGY_EXPORT_DIR}/administration_route.owl"
    )

    """Trimming the NCBITaxon"""

    logger.warning(f'Refactoring NCBITaxon.')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar extract --method STAR -i {ONTOLOGY_IMPORT_DIR}/ncbitaxon.owl \
            --term-file {ONTOLOGY_IMPORT_DIR}/ncbitaxon_terms.txt --copy-ontology-annotations true \
            --intermediates all --imports exclude -o {ONTOLOGY_EXPORT_DIR}/ncbitaxon_extracted.owl"
    )

    # Refactoring the ontology to include the re-grouping of bacteria
    os.system(
        f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_EXPORT_DIR}/ncbitaxon_extracted.owl \
            --template {TEMPLATE_DIR}/bacteria_bpo_tree.tsv merge \
            -i {ONTOLOGY_EXPORT_DIR}/ncbitaxon_extracted.owl --include-annotations true reduce --reasoner ELK \
            -o {ONTOLOGY_EXPORT_DIR}/organism.owl"
    )

    """Merging NCBITaxon and NCIT"""

    logger.warning(f'Merging ontologies')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar merge -i {ONTOLOGY_EXPORT_DIR}/administration_route.owl \
        -i {ONTOLOGY_EXPORT_DIR}/organism.owl --include-annotations false \
        annotate --annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
        -o {ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl"
    )

    """Trimming the EFO"""

    logger.warning(f'Refactoring EFO.')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar extract --method STAR -i {ONTOLOGY_IMPORT_DIR}/efo.owl \
        --term-file {ONTOLOGY_IMPORT_DIR}/efo_terms.txt --copy-ontology-annotations true \
        --intermediates all --imports exclude -o {ONTOLOGY_EXPORT_DIR}/efo_extracted.owl"
    )

    # logger.warning(f'Refactoring the mouse strain tree.')
    # os.system(
    #     f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_EXPORT_DIR}/efo_extracted.owl \
    #         --template {ONTOLOGY_IMPORT_DIR}/templates/mouse_strain_tree.tsv merge \
    #         -i {ONTOLOGY_EXPORT_DIR}/organism_bpo.owl -i {ONTOLOGY_EXPORT_DIR}/efo_extracted.owl \
    #         --include-annotations true reduce --reasoner ELK -o {ONTOLOGY_EXPORT_DIR}/organism_with_strains.owl"
    # )

    # logger.warning('Annotate the BPO ontology')
    # os.system(
    #     f"java -jar {LIB_DIR}/robot.jar annotate --input {ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl \
    #          --ontology-iri https://github.com/Fraunhofer-ITMP/bpo.owl \
    #          --version-iri https://github.com/Fraunhofer-ITMP/bpo-dev.owl \
    #          --annotation dc:title Bioassay_Protocol_Ontology \
    #          --annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
    #          --annotation dc:description An_ontology_for_bioassay_protocols \
    #          -o {ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl"
    # )

    # logger.warning(f'Reasoning the BPO ontology')
    # os.system(
    #     f"java -jar {LIB_DIR}/robot.jar materialize --reasoner ELK -i {ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl \
    #         reduce -o {ONTOLOGY_EXPORT_DIR}/route_organism_merged_reduced.owl"
    # )
    #
    # logger.warning(f'Generating the ROBOT report')
    # os.system(
    #     f"java -jar {LIB_DIR}/robot.jar report -i {ONTOLOGY_EXPORT_DIR}/route_organism_merged_reduced.owl \
    #         -o {ONTOLOGY_EXPORT_DIR}/route_organism_merged_report.tsv"
    # )


if __name__ == '__main__':
    main()
