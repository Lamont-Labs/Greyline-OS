#!/usr/bin/env bash
set -e

if [ ! -f dist/demo_exports/MD/nonfiction.md ]; then
  echo "Rendering first artifact ..."
  python cli/greyline_cli.py render --in src/pipelines/nonfiction_demo.yaml \
    --out dist/demo_exports/MD/nonfiction.md --prov SBOM
fi

echo "🧩 Verifying determinism for Greyline OS v3.3.4 ..."
FIRST=$(sha256sum dist/demo_exports/MD/nonfiction.md | awk '{print $1}')
sleep 1
python cli/greyline_cli.py render --in src/pipelines/nonfiction_demo.yaml \
  --out dist/demo_exports/MD/nonfiction.md --prov SBOM >/dev/null
SECOND=$(sha256sum dist/demo_exports/MD/nonfiction.md | awk '{print $1}')

if [ "$FIRST" != "$SECOND" ]; then
  echo "❌ Determinism check failed"
  echo "First : $FIRST"
  echo "Second: $SECOND"
  exit 1
fi

echo "✅ Determinism verified — hash $FIRST"
