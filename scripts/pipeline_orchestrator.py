import subprocess
import json
from datetime import datetime

steps = [
    "python scripts/data_generation/generate_data.py",
    "python scripts/ingestion/ingest_to_staging.py",
    "python scripts/quality_checks/validate_data.py",
    "python scripts/transformation/staging_to_production.py",
    "python scripts/transformation/load_to_warehouse.py",
]

start = datetime.now()
status = "success"

for cmd in steps:
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        status = "failed"
        break

report = {
    "start_time": start.isoformat(),
    "end_time": datetime.now().isoformat(),
    "status": status
}

with open("data/processed/pipeline_execution_report.json", "w") as f:
    json.dump(report, f, indent=4)
