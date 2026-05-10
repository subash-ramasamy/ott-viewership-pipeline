select
    content_id,
    content_name,
    platform,
    mention_count,
    sentiment_score,
    trending_rank,
    cast(recorded_date as date) as recorded_date
from {{ source('ott_viewership', 'social_engagement') }}