#!/bin/bash
# Quick test script for the WordPress migration environment

cd /mnt/c/Users/abhir/OneDrive/Desktop/Projects/wp_migration_tool
source wp_migration_venv/bin/activate

echo "=== Environment Test ==="
echo "Python version: $(python3 --version)"
echo "Pip version: $(pip --version)"

echo "=== Testing Playwright ==="
python3 -c "import playwright; print('✅ Playwright import successful')"

echo "=== Testing script files ==="
ls -la *.py *.sh

echo "=== Virtual environment location ==="
which python3
echo "Environment: $VIRTUAL_ENV"

echo "=== Test Complete ==="