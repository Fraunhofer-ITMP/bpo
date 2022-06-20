
# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://purl.obolibrary.org/obo
ONT=bpo
ONT_INF=bpo_inferred
ONT_BFO=bpo_bfo
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
SRCANOT=$(ONT)_annotated.owl
RELEASEDIR=../..
ROBOT= ../../bin/robot
OWLTOOLS= ../../bin/owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: sparql_test all_imports hancestro_annotated bfo_intermediate bfo_full $(ONT).owl $(ONT_INF).owl $(ONT_BFO).owl
#	$(ONT).obo 
test: sparql_test all
prepare_release: all
	cp $(ONT).owl $(ONT_INF).owl $(ONT_BFO).owl $(RELEASEDIR) &&\
	mkdir -p $(RELEASEDIR)/imports &&\
	cp imports/*.owl $(RELEASEDIR)/imports &&\
	cp imports/*.obo $(RELEASEDIR)/imports &&\
	git add $(RELEASEDIR)/imports/*.obo &&\
	git add $(RELEASEDIR)/imports/*.owl &&\
	(test -f subsets/*owl && cp subsets/* $(RELEASEDIR)/subsets && git add $(RELEASEDIR)/subsets/* || echo "no subsets") &&\
	echo "Release files are now in $(RELEASEDIR) - now yo.json',u should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# by default we use Elk to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo
$(ONT).owl: $(SRCANOT)
	$(ROBOT)  reason -i $< -r ELK relax reduce -r ELK annotate -O $(BASE)/$(ONT).owl -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
#$(ONT).obo: $(ONT).owl
#	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@
$(ONT_INF).owl: $(ONT).owl
	$(ROBOT) -v reason -s true -m false -r hermit -i $< -o $@
#$(ONT_BFO).owl: $(ONT).owl
#	$(ROBOT) -v reason -s true -m false -r hermit -i $< -o $@

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS = ncbitaxon ncit
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS))  imports/bfo_import.owl imports/pato_import.owl imports/mco_import.owl

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method STAR -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

imports/bfo_import.owl: mirror/bfo.owl imports/bfo_terms.txt
	$(ROBOT) extract -i $< -T imports/bfo_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/bfo_import.owl

imports/mco_import.owl: # mirror/pato.owl imports/obi_terms.txt - TODO: Find put what this does
	$(ROBOT) extract -i mirror/mco.owl -T imports/mco_terms.txt --method MIREOT --upper-term "obo:BFO_0000011" --lower-term "obo:MCO_0000368" --lower-term "obo:MCO_0000366" -O $(BASE)/$@ -o $@
.PRECIOUS: imports/mco_import.owl

imports/pato_import.owl: # mirror/pato.owl imports/obi_terms.txt - TODO: Find put what this does
	$(ROBOT) extract -i mirror/pato.owl -T imports/pato_terms.txt --method MIREOT --upper-term "obo:BFO_0000001" --lower-term "obo:PATO_0000384" --lower-term "obo:PATO_0000383" -O $(BASE)/$@ -o $@
.PRECIOUS: imports/pato_import.owl

# Add '--check false' flag if your OWL is not obo-strict
#imports/%_import.obo: imports/%_import.owl
#	$(ROBOT) convert -f -i $< -o $@

# clone remote ontology locally, perfoming some excision of relations and annotations
mirror/%.owl: $(SRC)
	$(ROBOT) convert -I $(OBO)/$*.owl -o $@
.PRECIOUS: mirror/%.owl


# ----------------------------------------
# Annotate HANCESTRO with xrefs
# ----------------------------------------
# Use a template file to build annotations
#

hancestro_annotated: $(SRC)
	$(ROBOT) template --input $<  --prefix "dbpedia: http://dbpedia.org/resource/" --prefix "go: http://www.geneontology.org/formats/oboInOwl#" --prefix "obo http://purl.obolibrary.org/obo/" --template ../templates/gaz_xrefs.tsv merge --input $< --include-annotations true annotate --ontology-iri http://purl.obolibrary.org/obo/hancestro --output $(SRCANOT)


# ----------------------------------------
# Build HANCESTRO-BFO 
# ----------------------------------------
# Use a template file to build a
#

bfo_intermediate: 
	$(ROBOT) template --input $(SRCANOT) --prefix "geo: http://purl.obolibrary.org/obo/" --prefix "hancestro: http://purl.obolibrary.org/obo/" --prefix "bfo: http://purl.obolibrary.org/obo/" --prefix "obi: http://purl.obolibrary.org/obo/" --template ../templates/upper_level.tsv merge --input $(SRCANOT) --include-annotations true reduce --reasoner ELK --output hancestro_bfo_intermediate.owl 


bfo_full: 
	$(ROBOT) merge --input hancestro_bfo_intermediate.owl --input imports/bfo_import.owl --input imports/ncbi_import.owl --input imports/ncit_import.owl --input imports/mco_import.owl  --input imports/pato_import.owl --include-annotations true annotate --ontology-iri http://purl.obolibrary.org/obo/bpo reduce --reasoner ELK --output bpo_bfo.owl




# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl $(ONT_INF).owl $(ONT_BFO).owl
	#$(ONT).obo 	
#	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports
	cp $^ $(RELEASEDIR) 

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live
VCHECKS = equivalent-classes trailing-whitespace owldef-self-reference xref-syntax nolabels

# run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	$(ROBOT) verify -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	$(ROBOT) query -f tsv -i $< $(REPORT_ARGS)

# ----------------------------------------
# Docker (experimental)
# ----------------------------------------
IM=build-$(ONT)
build-docker:
	docker build -t $(ONT) .
