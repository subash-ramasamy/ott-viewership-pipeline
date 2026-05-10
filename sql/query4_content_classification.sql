-- Cross Platform Content Intelligence

WITH ott_summary AS (
    SELECT
        content_id,
        content_name,
        ROUND(AVG(completion_pct), 1)  AS avg_completion,
        COUNT(DISTINCT user_id)        AS unique_viewers
    FROM `ott-viewership-pipeline.ott_viewership.ott_events`
    WHERE user_id != 'ANONYMOUS'
    GROUP BY content_id, content_name
),
social_summary AS (
    SELECT
        content_id,
        SUM(mention_count)              AS total_mentions,
        ROUND(AVG(sentiment_score), 3)  AS avg_sentiment
    FROM `ott-viewership-pipeline.ott_viewership.social_engagement`
    GROUP BY content_id
)
SELECT
    o.content_name,
    o.unique_viewers,
    o.avg_completion,
    s.total_mentions,
    s.avg_sentiment,
    CASE
        WHEN s.total_mentions > 8700000
         AND o.avg_completion < 64
        THEN 'Hook Fail'
        WHEN s.total_mentions > 8700000
         AND o.avg_completion >= 64
        THEN 'Star Content'
        WHEN s.total_mentions < 8500000
         AND o.avg_completion >= 64
        THEN 'Hidden Gem'
        ELSE 'Average Performer'
    END AS content_classification
FROM ott_summary o
JOIN social_summary s
  ON o.content_id = s.content_id
ORDER BY s.total_mentions DESC;
