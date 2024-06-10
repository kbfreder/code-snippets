SELECT table_name, column_name, is_nullable, character_maximum_length
FROM information_schema.columns
WHERE data_type like 'character %' AND character_maximum_length > 65000
    AND table_name not like 'aq_%' AND table_name not like 'aud_%'
ORDER BY table_name