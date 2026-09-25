# OKRs

### schedule_adherence
- **Target**: the `reach:api-mine` cron runs within ±1h of its `0 4 * * *` schedule on ≥95% of days per month.
- **Measurement**: compare wall-clock api-mine timestamps in `evidence.jsonl` (and its journal) against the schedule; runs outside the ±1h window are misses. `reach.query` runs are demand-driven and excluded — api-mine is the skill's only scheduled job.

### data_integrity
- **Target**: Zero silent data loss events per month.
- **Measurement**: All query runs (including no-ops and errors) must have a corresponding entry in `evidence.jsonl` and `usage.jsonl`. Gaps detected during recovery audit are violations.
