select
    show_id,
    show_name,
    channel,
    genre,
    language,
    cast(air_date as date) as air_date,
    city,
    city_tier,
    ratings_million,
    week_number
from {{ source('ott_viewership', 'barc_ratings') }}