-- High Value User Identification

with user_totals as (
    select
        user_id,
        count(distinct content_id)    as content_variety,
        sum(watch_duration_mins)      as total_watch_mins,
        round(avg(completion_pct), 1) as avg_completion,
        max(subscription_tier)        as subscription_tier
    from {{ ref('stg_ott_events') }}
    where user_id != 'ANONYMOUS'
    group by user_id
),
platform_avg as (
    select
        round(avg(total_watch_mins), 1)   as avg_watch_mins,
        round(avg(content_variety), 1)    as avg_content_variety
    from user_totals
)
select
    u.user_id,
    u.subscription_tier,
    u.total_watch_mins,
    u.content_variety,
    u.avg_completion,
    round(u.total_watch_mins - p.avg_watch_mins, 1) as above_avg_by_mins,
    case
        when u.subscription_tier = 'Free'
         and u.total_watch_mins > p.avg_watch_mins
        then 'Convert to Paid — High Engagement'
        when u.subscription_tier in ('Basic', 'Premium')
         and u.total_watch_mins > p.avg_watch_mins
        then 'Upsell to Annual — Loyal User'
        when u.total_watch_mins < p.avg_watch_mins
        then 'Re-engage — Below Average'
        else 'Monitor'
    end as user_action
from user_totals u, platform_avg p
where u.total_watch_mins > p.avg_watch_mins
order by u.total_watch_mins desc