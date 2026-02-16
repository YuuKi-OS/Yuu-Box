#!/bin/bash
set -e

echo "Building YuuBox (Rust + Python)"
echo ""

echo "Step 1: Build Rust core..."
cd yuubox-core
cargo build --release
cd ..

echo ""
echo "Step 2: Build Python wheel with maturin..."
maturin build --release

echo ""
echo "Step 3: Install locally..."
pip install target/wheels/*.whl

echo ""
echo "✅ Build complete!"
echo ""
echo "Usage:"
echo "  yuubox run script.py"
echo "  python -c 'from yuubox import YuuBox; box = YuuBox()'"
