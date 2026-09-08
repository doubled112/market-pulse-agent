"""
Orchestrator
Job: run Fetch -> Process -> Publish in sequence, handling failures
between stages so one bad stage doesn't corrupt or silently skip the rest.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime, timezone

sys.path.append(str(Path(__file__).resolve().parent))

import fetch_stage
import process_stage
import publish_stage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("orchestrator")


def run_stage(name, func):
    """Run a single stage, log the outcome, and re-raise on failure
    so the orchestrator can decide what to do next."""
    log.info(f"Starting stage: {name}")
    try:
        result = func()
        log.info(f"Stage succeeded: {name}")
        return result
    except Exception as e:
        log.error(f"Stage failed: {name} — {e}")
        raise


def main():
    started_at = datetime.now(timezone.utc).isoformat()
    log.info(f"Orchestration run started at {started_at}")

    try:
        run_stage("fetch", fetch_stage.fetch_and_save)
    except Exception:
        log.error("Fetch failed — aborting run. Nothing downstream can proceed without fresh data.")
        sys.exit(1)

    try:
        run_stage("process", process_stage.process)
    except Exception:
        log.error("Process failed — raw data exists but wasn't transformed. Skipping publish to avoid pushing stale data.")
        sys.exit(1)

    try:
        run_stage("publish", lambda: (publish_stage.publish(), publish_stage.git_commit_and_push()))
    except Exception:
        log.error("Publish failed — data was fetched and processed but not pushed. Will retry on next scheduled run.")
        sys.exit(1)

    log.info("Orchestration run completed successfully.")


if __name__ == "__main__":
    main()