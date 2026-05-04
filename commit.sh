#!/bin/bash
# Rogue Bachata — quick commit & push
# Usage:  ./commit.sh "your commit message"
# If no message is supplied, you'll be prompted.

set -e
cd "$(dirname "$0")"

MSG="$1"
if [ -z "$MSG" ]; then
  echo "Commit message: "
  read MSG
fi
if [ -z "$MSG" ]; then
  echo "Aborted: empty message."
  exit 1
fi

echo "── git status ──"
git status --short

echo ""
echo "── staging all changes ──"
git add -A

echo ""
echo "── committing ──"
git commit -m "$MSG"

echo ""
echo "── pushing ──"
git push

echo ""
echo "✓ Done."
