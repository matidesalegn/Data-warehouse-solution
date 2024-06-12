-- models/transformed_data.sql
with cleaned as (
    select *
    from {{ ref('cleaned_data') }}
)

select
    message_id,
    sender_id,
    upper(message_text) as message_text_uppercase,
    channel
from cleaned