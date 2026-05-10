-- Week Over Week TV Rating Trends

WITH weekly_avg AS (
    SELECT
        show_name,
        channel,
        week_number,
        ROUND(AVG(ratings_million), 2) AS avg_week_rating
    FROM `ott-viewership-pipeline.ott_viewership.barc_ratings`
    GROUP BY show_name, channel, week_number
),
with_lag AS (
    SELECT
        show_name,
        channel,
        week_number,
        avg_week_rating,
        LAG(avg_week_rating) OVER (
            PARTITION BY show_name
            ORDER BY week_number
        )                               AS prev_week_rating
    FROM weekly_avg
)
SELECT
    show_name,
    channel,
    week_number,
    avg_week_rating,
    prev_week_rating,
    ROUND(avg_week_rating - prev_week_rating, 2)    AS wow_change,
    CASE
        WHEN avg_week_rating > prev_week_rating THEN 'Growing'
        WHEN avg_week_rating < prev_week_rating THEN 'Declining'
        WHEN prev_week_rating IS NULL      THEN 'First Week'
        ELSE                                    'Stable'
    END                                        AS trend
FROM with_lag
ORDER BY show_name, week_number;