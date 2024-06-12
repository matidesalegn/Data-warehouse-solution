-- models/cleaned_data.sql
with raw as (
    select *
    from {{ source('public', 'medical_data') }}
)

select
    message_id,
    sender_id,
    message_text,
    channel
from raw