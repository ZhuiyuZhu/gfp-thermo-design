#!/bin/bash
# GFP Design Pipeline Runner

set -e

echo "=========================================="
echo "GFP Design Pipeline"
echo "=========================================="

# 检查环境
echo "[1/3] Checking environment..."
python -c "import torch; import esm; import pandas; print('Dependencies OK')"

# Step 1: ESM-2突变扫描 (可选，需要GPU/较长时间)
if [ "$1" == "--full" ]; then
    echo "[2/3] Running ESM-2 mutation scan..."
    python scripts/01_esm2_mutation_scan.py --output results/esm2_scores.csv
else
    echo "[2/3] Skipping ESM-2 scan (use --full to enable)"
fi

# Step 2: 序列组装 (核心)
echo "[3/3] Generating sequences..."
python scripts/02_sequence_assembler_v2_1.py

echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "Submission file: results/submission_final.csv"
echo "=========================================="
