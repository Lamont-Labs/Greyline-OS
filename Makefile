# Greyline OS Demo Makefile
VERSION = 3.3.4
DATE = 2025-10-05

.PHONY: demo verify sbom clean

demo:
	python cli/greyline_cli.py render --in src/pipelines/nonfiction_demo.yaml \
	  --out dist/demo_exports/MD/nonfiction.md --prov SBOM

verify:
	bash verify.sh

sbom:
	python cli/greyline_cli.py sbom --out SBOM/sbom.cdx.json

clean:
	rm -rf dist/demo_exports/* SBOM/checksums.csv SBOM/provenance.json
