#!/bin/sh
# ======================================
# Simple automated git command sequence
# ======================================
# Cleanup any OSX folders
python cleanup.py
# Push changes
git add -A
git commit -m $1
git push origin
# Reinstall
pip install -e .