-- Top Performing Content by Completion Rate

with content_summary as (
    select
        content_name,
        content_type,
        count(distinct user_id)            as unique_viewers,
        round(avg(completion_pct), 2)      as avg_completion,
        round(sum(watch_duration_mins), 0) as total_watch_mins
    from {{ ref('stg_ott_events') }}
    where user_id != 'ANONYMOUS'
    group by content_name, content_type
),
ranked as (
    select
        *,
        rank() over (
            partition by content_type
            order by avg_completion desc
        ) as completion_rank
    from content_summary
)
select
    content_type,
    content_name,
    unique_viewers,
    avg_completion,
    total_watch_mins,
    completion_rank
from ranked
where completion_rank <= 3
order by content_type, completion_rank