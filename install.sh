#!/bin/bash
set -e

echo "Installing YuuBox..."

# Install Rust if not present
if ! command -v cargo &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

# Install maturin
pip install maturin

# Build and install
./build.sh

echo ""
echo "✅ Installation complete!"
echo ""
echo "Test with:"
echo "  yuubox run examples/basic_usage.py"
