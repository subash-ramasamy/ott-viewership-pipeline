select
    event_id,
    user_id,
    content_id,
    content_name,
    content_type,
    watch_duration_mins,
    completion_pct,
    device_type,
    subscription_tier,
    city,
    city_tier,
    cast(event_timestamp as timestamp) as watched_at

from {{ source('ott_viewership', 'ott_events') }}