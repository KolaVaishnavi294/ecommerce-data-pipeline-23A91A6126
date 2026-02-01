SELECT COUNT(*) AS failed_runs
FROM pipeline_execution_log
WHERE status = 'failed';
