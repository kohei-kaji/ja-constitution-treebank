#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

uv run src/depparse.py data/preamble.txt silver/preamble-ginza.conllu
uv run src/depparse.py data/constitution.txt silver/constitution-ginza.conllu
