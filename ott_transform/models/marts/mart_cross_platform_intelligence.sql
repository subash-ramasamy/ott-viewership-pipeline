-- Cross Platform Content Intelligence

with ott_summary as (
    select
        content_id,
        content_name,
        round(avg(completion_pct), 1) as avg_completion,
        count(distinct user_id)       as unique_viewers
    from {{ ref('stg_ott_events') }}
    where user_id != 'ANONYMOUS'
    group by content_id, content_name
),
social_summary as (
    select
        content_id,
        sum(mention_count)             as total_mentions,
        round(avg(sentiment_score), 3) as avg_sentiment
    from {{ ref('stg_social_engagement') }}
    group by content_id
)
select
    o.content_name,
    o.unique_viewers,
    o.avg_completion,
    s.total_mentions,
    s.avg_sentiment,
    case
        when s.total_mentions > 8700000
         and o.avg_completion < 64
        then 'Hook Fail'
        when s.total_mentions > 8700000
         and o.avg_completion >= 64
        then 'Star Content'
        when s.total_mentions < 8500000
         and o.avg_completion >= 64
        then 'Hidden Gem'
        else 'Average Performer'
    end as content_classification
from ott_summary o
join social_summary s
    on o.content_id = s.content_id
order by s.total_mentions desc