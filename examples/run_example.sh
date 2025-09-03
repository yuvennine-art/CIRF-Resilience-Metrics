#!/usr/bin/env bash
set -euo pipefail

python src/cirf_pipeline.py --input examples/sample_logs --output results
echo "Done. See ./results/ for outputs."
