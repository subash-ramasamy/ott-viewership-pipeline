-- Top Performing Content by Completion Rate

WITH content_summary AS (
    SELECT
        content_name,
        content_type,
        COUNT(DISTINCT user_id)              AS unique_viewers,
        ROUND(AVG(completion_pct), 2)        AS avg_completion,
        ROUND(SUM(watch_duration_mins), 0)   AS total_watch_mins
    FROM `ott-viewership-pipeline.ott_viewership.ott_events`
    WHERE user_id != 'ANONYMOUS'
    GROUP BY content_name, content_type
),
ranked AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY content_type
            ORDER BY avg_completion DESC
        ) AS completion_rank
    FROM content_summary
)
SELECT
    content_type,
    content_name,
    unique_viewers,
    avg_completion,
    total_watch_mins,
    completion_rank
FROM ranked
WHERE completion_rank <= 3
ORDER BY content_type, completion_rank;