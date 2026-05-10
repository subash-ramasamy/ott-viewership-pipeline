-- High Value User Identification

WITH user_totals AS (
    SELECT
        user_id,
        COUNT(DISTINCT content_id)      AS content_variety,
        SUM(watch_duration_mins)        AS total_watch_mins,
        ROUND(AVG(completion_pct), 1)   AS avg_completion,
        MAX(subscription_tier)          AS subscription_tier
    FROM `ott-viewership-pipeline.ott_viewership.ott_events`
    WHERE user_id != 'ANONYMOUS'
    GROUP BY user_id
),
platform_avg AS (
    SELECT
        ROUND(AVG(total_watch_mins), 1) AS avg_watch_mins,
        ROUND(AVG(content_variety), 1)  AS avg_content_variety
    FROM user_totals
)
SELECT
    u.user_id,
    u.subscription_tier,
    u.total_watch_mins,
    u.content_variety,
    u.avg_completion,
    ROUND(u.total_watch_mins - p.avg_watch_mins, 1) AS above_avg_by_mins,
    CASE
        WHEN u.subscription_tier = 'Free'
         AND u.total_watch_mins > p.avg_watch_mins
        THEN 'Convert to Paid — High Engagement'
        WHEN u.subscription_tier IN ('Basic', 'Premium')
         AND u.total_watch_mins > p.avg_watch_mins
        THEN 'Upsell to Annual — Loyal User'
        WHEN u.total_watch_mins < p.avg_watch_mins
        THEN 'Re-engage — Below Average'
        ELSE 'Monitor'
    END                                             AS user_action
FROM user_totals u, platform_avg p
WHERE u.total_watch_mins > p.avg_watch_mins
ORDER BY u.total_watch_mins DESC
;