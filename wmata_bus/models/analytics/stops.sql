{{ config(materialized='table') }}

with arrival_times_at_stopid as (
      select trip_id, 
      stop_id,
            CONCAT(
            CASE LENGTH(SPLIT(arrival_time, ':')[0]) 
                  WHEN 1 THEN '0'
                  WHEN 0 THEN '00'
                  ELSE ''
            END,
            SPLIT(arrival_time, ':')[0], ':',
            CASE LENGTH(CAST(TRUNC(CAST (SPLIT(arrival_time, ':')[1] AS INTEGER) / 10) * 10 AS STRING)) 
                  WHEN 1 THEN '0'
                  WHEN 0 THEN '00'
                  ELSE ''
            END,
            CAST(TRUNC(CAST (SPLIT(arrival_time, ':')[1] AS INTEGER) / 10) * 10 AS STRING) , ':',
            '00') 
       as stop_time
FROM {{ source('stage', 'stop_times') }} ),

stop_counts as (
      SELECT atstop.stop_id, atstop.stop_time, count(1) as stop_count FROM arrival_times_at_stopid atstop
      GROUP BY 1,2 
      ORDER BY 1,2
)

SELECT stop_counts.*, stops.stop_code, stops.stop_name, ST_GEOGPOINT(stops.stop_lon, stops.stop_lat) as location FROM stop_counts 
INNER JOIN {{ source('stage', 'stops') }} stops
ON stop_counts.stop_id = stops.stop_id
ORDER BY stop_counts.stop_id, stop_counts.stop_time