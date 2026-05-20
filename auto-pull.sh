#!/bin/bash

# Auto-pull script for /Users/tbaum/src/texts
# Checks every 10 seconds (6 times) if a git pull is needed

REPO_DIR="/Users/tbaum/src/texts"
LOG_FILE="$REPO_DIR/.auto-pull.log"

cd "$REPO_DIR" || exit 1

# Log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if pull is needed and execute if necessary
check_and_pull() {
    # Fetch latest changes from remote (quiet mode)
    git fetch origin --quiet 2>/dev/null || return 1

    # Get current local commit hash
    LOCAL=$(git rev-parse HEAD)

    # Get remote tracking branch commit hash
    REMOTE=$(git rev-parse @{upstream} 2>/dev/null)

    # If remote is different from local, pull is needed
    if [ "$LOCAL" != "$REMOTE" ]; then
        return 0  # Pull needed
    else
        return 1  # Already up-to-date
    fi
}

log "Script started"

# Run 6 checks over ~60 seconds (every 10 seconds)
for i in {1..6}; do
    if check_and_pull; then
        log "Changes detected, pulling..."
        if git pull origin "$(git branch --show-current)" 2>&1 | tee -a "$LOG_FILE"; then
            log "Pull successful"
        else
            log "Pull failed"
        fi
    fi

    # Sleep 10 seconds before next check (skip on last iteration)
    if [ $i -lt 6 ]; then
        sleep 10
    fi
done

log "Script completed"
