#!/bin/bash
# AI Video Market Watch — Daily Runner (launchd wrapper)
# Bu script launchd tarafından günlük çağrılır.

export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

PROJECT_DIR="/Users/yucezerey/growingo Dropbox/yuce zerey/@YZ - AI/@Antigravity/@YZDrive/@AI Yapım/@AI Video Market Watch"
LOGFILE="$PROJECT_DIR/logs/vmw-daily.log"

mkdir -p "$PROJECT_DIR/logs"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') — VMW Daily Start =====" >> "$LOGFILE"

cd "$PROJECT_DIR" && python3 scripts/run_daily.py >> "$LOGFILE" 2>&1

echo "===== $(date '+%Y-%m-%d %H:%M:%S') — VMW Daily End =====" >> "$LOGFILE"
echo "" >> "$LOGFILE"
