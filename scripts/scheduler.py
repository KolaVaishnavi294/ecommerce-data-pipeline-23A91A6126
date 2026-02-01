import schedule
import time
import subprocess

schedule.every().day.at("02:00").do(
    lambda: subprocess.run(["python", "scripts/pipeline_orchestrator.py"])
)

while True:
    schedule.run_pending()
    time.sleep(60)
