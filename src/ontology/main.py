# -*- coding: utf-8 -*-

"""File to create th BPO ontology."""

import logging
import os

ONTOLOGY_IMPORT_DIR = 'imports'
LIB_DIR = '../../bin'
ONTOLOGY_EXPORT_DIR = '../../imports'
TEMPLATE_DIR = '../templates'
REPORT_DIR = 'reports'
RELEASE_DIR = '../../release'

os.makedirs(ONTOLOGY_EXPORT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

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


def main(
    version: str
):
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

    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/ncit_extracted.owl'):
        logger.warning(f'Refactoring NCIT')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar extract --method STAR -i {ONTOLOGY_IMPORT_DIR}/ncit.owl \
                --term-file {ONTOLOGY_IMPORT_DIR}/ncit_terms.txt --copy-ontology-annotations true --intermediates all \
                --imports exclude -o {ONTOLOGY_IMPORT_DIR}/ncit_extracted.owl"
        )

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/administration_route.owl'):
        # Refactoring the NCIT ontology to BFO format using VO tree
        os.system(
            f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_IMPORT_DIR}/ncit_extracted.owl \
                --template {TEMPLATE_DIR}/ncit_vo_tree.tsv merge -i {ONTOLOGY_IMPORT_DIR}/ncit_extracted.owl \
                --include-annotations true reduce --reasoner ELK -o {ONTOLOGY_EXPORT_DIR}/administration_route.owl"
        )

    """Trimming the NCBITaxon"""

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/organism.owl'):
        logger.warning(f'Refactoring NCBITaxon.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar extract --method STAR -i {ONTOLOGY_IMPORT_DIR}/ncbitaxon.owl \
                --term-file {ONTOLOGY_IMPORT_DIR}/ncbitaxon_terms.txt --copy-ontology-annotations true \
                --intermediates all --imports exclude -o {ONTOLOGY_IMPORT_DIR}/ncbitaxon_extracted.owl"
        )

        # Refactoring the ontology to include the re-grouping of bacteria
        os.system(
            f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_IMPORT_DIR}/ncbitaxon_extracted.owl \
                --template {TEMPLATE_DIR}/bacteria_bpo_tree.tsv merge \
                -i {ONTOLOGY_IMPORT_DIR}/ncbitaxon_extracted.owl --include-annotations true reduce --reasoner ELK \
                -o {ONTOLOGY_EXPORT_DIR}/organism.owl"
        )

    """Merging NCBITaxon and NCIT"""

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl'):
        logger.warning(f'Merging ontologies')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar merge -i {ONTOLOGY_EXPORT_DIR}/administration_route.owl \
            -i {ONTOLOGY_EXPORT_DIR}/organism.owl --include-annotations false \
            annotate --annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
            -o {ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl"
        )

    """Trimming the EFO"""

    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/efo_extracted.owl'):
        logger.warning(f'Refactoring EFO.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar extract --method STAR -i {ONTOLOGY_IMPORT_DIR}/efo.owl \
            --term-file {ONTOLOGY_IMPORT_DIR}/efo_terms.txt --copy-ontology-annotations false \
            --intermediates none --imports exclude -o {ONTOLOGY_IMPORT_DIR}/efo_extracted.owl"
        )

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/route_organism_efo_merged.owl'):
        os.system(
            f"java -jar {LIB_DIR}/robot.jar merge \
            -i {ONTOLOGY_EXPORT_DIR}/route_organism_merged.owl -i {ONTOLOGY_IMPORT_DIR}/efo_extracted.owl \
            --include-annotations false annotate --annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
             -o {ONTOLOGY_EXPORT_DIR}/route_organism_efo_merged.owl"
        )

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/organism_with_strains.owl'):
        logger.warning(f'Refactoring the mouse strain tree.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_EXPORT_DIR}/route_organism_efo_merged.owl \
            --template {TEMPLATE_DIR}/mouse_strain_tree.tsv merge \
            -i {ONTOLOGY_EXPORT_DIR}/route_organism_efo_merged.owl \
            --include-annotations false reduce --reasoner ELK -o {ONTOLOGY_EXPORT_DIR}/organism_with_strains.owl"
        )

    """Creating PATO tree and Merging with existing tree"""

    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/pato_extracted.owl'):
        logger.warning(f'Creating PATO subtree.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar extract --method MIREOT -i {ONTOLOGY_IMPORT_DIR}/pato.owl \
            --upper-term PATO:0000001 --lower-term PATO:0000384 --lower-term PATO:0000383 \
            --copy-ontology-annotations false --intermediates all \
            --imports exclude -o {ONTOLOGY_IMPORT_DIR}/pato_extracted.owl"
        )

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/organism_sex_merged.owl'):
        logger.warning(f'Merging the PATO tree.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar merge \
            -i {ONTOLOGY_EXPORT_DIR}/organism_with_strains.owl -i {ONTOLOGY_IMPORT_DIR}/pato_extracted.owl \
            --include-annotations false annotate --annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
             -o {ONTOLOGY_EXPORT_DIR}/organism_sex_merged.owl"
        )

    """Creating IDO subtree and Merging with existing ontology"""

    if not os.path.exists(f'{ONTOLOGY_IMPORT_DIR}/ido_extracted.owl'):
        logger.warning(f'Creating IDO subtree.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar extract --method MIREOT -i {ONTOLOGY_IMPORT_DIR}/ido.owl \
                --lower-term IDO:0001009 --copy-ontology-annotations false --intermediates all \
                --imports exclude -o {ONTOLOGY_IMPORT_DIR}/ido_extracted.owl"
        )

    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/organism_sex_ido_merged.owl'):
        logger.warning(f'Rearranging IDO subtree.')
        os.system(
            f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_IMPORT_DIR}/ido_extracted.owl \
                --template {TEMPLATE_DIR}/immunosuppression_tree.tsv merge \
                -i {ONTOLOGY_EXPORT_DIR}/organism_sex_merged.owl --include-annotations false \
                reduce --reasoner ELK -o {ONTOLOGY_EXPORT_DIR}/organism_sex_ido_merged.owl"
        )

    """Refactoring ontology to BFO format"""
    if not os.path.exists(f'{ONTOLOGY_EXPORT_DIR}/bpo_{version}.owl'):
        os.system(
            f"java -jar {LIB_DIR}/robot.jar template -i {ONTOLOGY_EXPORT_DIR}/organism_sex_ido_merged.owl \
                --template {TEMPLATE_DIR}/upper_level_class.tsv merge \
                -i {ONTOLOGY_EXPORT_DIR}/organism_sex_ido_merged.owl \
                --include-annotations false reduce --reasoner ELK -o {ONTOLOGY_EXPORT_DIR}/bpo_{version}.owl"
        )

    logger.warning('Annotate the BPO ontology')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar annotate --input {ONTOLOGY_EXPORT_DIR}/bpo_{version}.owl \
             --ontology-iri https://github.com/Fraunhofer-ITMP/bpo.owl \
             --version-iri https://github.com/Fraunhofer-ITMP/bpo-0.0.1.owl \
             --annotation dc:title 'Bioassay Protocol Ontology' \
             --annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
             --annotation dc:description 'An ontology for bioassay protocols' \
             -o {ONTOLOGY_EXPORT_DIR}/bpo_annotated.owl"
    )

    os.makedirs(f'{RELEASE_DIR}/v{version}')

    logger.warning(f'Reasoning merge')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar materialize --reasoner ELK \
        -i {ONTOLOGY_EXPORT_DIR}/bpo_{version}_annotated.owl \
        reduce -o {RELEASE_DIR}/v{version}/bpo.owl"
    )

    logger.warning(f'Generating report')
    os.system(
        f"java -jar {LIB_DIR}/robot.jar report -i {RELEASE_DIR}/v{version}/bpo.owl \
        -o {REPORT_DIR}/report_bpo.tsv"
    )

    # Exporting to different formats
    os.system(
        f"java -jar {LIB_DIR}/robot.jar export --input bpo.owl --header 'ID|LABEL|SubClasses' \
         --format tsv --export {RELEASE_DIR}/v{version}/bpo.tsv"
    )

    os.system(
        f'java -jar {LIB_DIR}/robot.jar convert --input bpo.owl --output {RELEASE_DIR}/v{version}/bpo.obo'
    )


if __name__ == '__main__':
    main(version='0.0.1')
