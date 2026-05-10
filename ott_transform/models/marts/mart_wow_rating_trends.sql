-- Week Over Week TV Rating Trends

with weekly_avg as (
    select
        show_name,
        channel,
        week_number,
        round(avg(ratings_million), 2) as avg_week_rating
    from {{ ref('stg_barc_ratings') }}
    group by show_name, channel, week_number
),
with_lag as (
    select
        show_name,
        channel,
        week_number,
        avg_week_rating,
        lag(avg_week_rating) over (
            partition by show_name
            order by week_number
        ) as prev_week_rating
    from weekly_avg
)
select
    show_name,
    channel,
    week_number,
    avg_week_rating,
    prev_week_rating,
    round(avg_week_rating - prev_week_rating, 2) as wow_change,
    case
        when avg_week_rating > prev_week_rating then 'Growing'
        when avg_week_rating < prev_week_rating then 'Declining'
        when prev_week_rating is null           then 'First Week'
        else                                         'Stable'
    end as trend
from with_lag
order by show_name, week_number