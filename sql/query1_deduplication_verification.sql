-- Deduplication verification

WITH clean_check AS (
    SELECT
        COUNT(DISTINCT event_id)  AS unique_events,
        COUNT(*)                  AS total_rows
    FROM `your-project-id.ott_viewership.ott_events`
)
SELECT
    unique_events,
    total_rows,
    total_rows - unique_events AS duplicate_count,
    ROUND(
        (total_rows - unique_events) * 100.0 / total_rows
    , 2)                        AS duplicate_pct
FROM clean_check;