import subprocess
import time
import yaml
import os
from pathlib import Path
from logger import get_logger
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path("config/config.yaml")

logger = get_logger("PIPELINE")


def run_command(command: str):
    logger.info(f"Running command: {command}")
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(f"Command failed: {command}")

    logger.info(result.stdout)


def main():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    retries = config["pipeline"].get("retries", 1)
    log_level = config["pipeline"].get("log_level", "INFO")

    logger.info(f"Pipeline started with retries={retries}, log_level={log_level}")

    steps = [
        ("data_generation", "python scripts/data_generation/generate_data.py"),
        ("ingestion", "python scripts/ingestion/load_to_staging.py"),
        ("quality_checks", "python scripts/quality_checks/validate_data.py"),
        ("load_production", "python scripts/transformation/load_to_production.py"),
        ("load_warehouse", "python scripts/transformation/load_to_warehouse.py"),
    ]

    for step_name, command in steps:
        logger.info(f"=== START STEP: {step_name} ===")

        attempt = 0
        while attempt <= retries:
            try:
                run_command(command)
                logger.info(f"=== SUCCESS: {step_name} ===")
                break
            except Exception as e:
                attempt += 1
                logger.warning(f"Attempt {attempt} failed for {step_name}: {e}")

                if attempt > retries:
                    logger.error(f"=== PIPELINE FAILED AT STEP: {step_name} ===")
                    raise

                time.sleep(5)

    logger.info("PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
