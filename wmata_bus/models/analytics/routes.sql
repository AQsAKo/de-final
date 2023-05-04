{{ config(materialized='table') }}

with routes_ordered as (
  SELECT shape_id, ST_GEOGPOINT(shape_pt_lon, shape_pt_lat) as geopoint FROM {{ source('stage', 'shapes') }}
  ORDER BY shape_id, shape_pt_sequence
),
routes_geometry as (
  SELECT shape_id, ARRAY_AGG(geopoint) as geometry FROM routes_ordered 
  group by shape_id 
)

SELECT shape_id, ST_MAKELINE(geometry) as shape_geometry FROM routes_geometry 
ORDER BY shape_id