-- models/cleaned_data.sql
with raw as (
    select *
    from {{ source('public', 'data_warehouse') }}
)

select
    message_id,
    sender_id,
    message_text,
    channel
from raw