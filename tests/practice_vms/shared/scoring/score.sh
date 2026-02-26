#!/bin/bash

SCORE=0
MAX_SCORE=0
LOG="/opt/scoring/score.log"
HTML_OUTPUT="/opt/scoring/score.html"
CHECKS_HTML=""
SYSTEM_TYPE="Unknown"

echo "Scoring run at $(date)" > $LOG

# Detect system type
if [[ -f /etc/lsb-release ]]; then
  SYSTEM_TYPE="Ubuntu"
  source /opt/scoring/checks/ubuntu.sh
else
  SYSTEM_TYPE="Linux Mint"
  source /opt/scoring/checks/mint.sh
fi

echo "FINAL SCORE: $SCORE / $MAX_SCORE" | tee -a $LOG

# Calculate progress percentage (safe division)
if [ $MAX_SCORE -gt 0 ]; then
  PROGRESS=$((SCORE * 100 / MAX_SCORE))
else
  PROGRESS=0
fi

# Generate timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Generate HTML file with results
sed -e "s|\[\[SYSTEM\]\]|$SYSTEM_TYPE|g" \
    -e "s|\[\[SCORE\]\]|$SCORE / $MAX_SCORE|g" \
    -e "s|\[\[PROGRESS\]\]|$PROGRESS|g" \
    -e "s|\[\[TIMESTAMP\]\]|$TIMESTAMP|g" \
    -e "s|\[\[CHECKS\]\]|$CHECKS_HTML|g" \
    /opt/scoring/score.html > $HTML_OUTPUT

chmod 644 $HTML_OUTPUT
