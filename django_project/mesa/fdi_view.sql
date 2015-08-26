/*SELECT 
  mesa_fdipoint.id,
  mesa_fdiforecast.fdi_value,
  TRUE AS is_forecast
FROM 
  public.mesa_fdipoint 
  INNER JOIN public.mesa_fdiforecast ON mesa_fdiforecast.fdi_point_id = mesa_fdipoint.id
UNION
SELECT 
  mesa_fdipoint.id,
  mesa_fdimeasurement.fdi_value,
  FALSE AS is_forecast
FROM 
  public.mesa_fdipoint 
  INNER JOIN public.mesa_fdimeasurement ON mesa_fdimeasurement.fdi_point_id = mesa_fdipoint.id
*/

SELECT
          mesa_fdipoint.id, 
          mesa_fdipoint.name, 
          mesa_fdipoint.type, 
          mesa_fdipoint.station_name, 
          mesa_fdimeasurement.fdi_value, 
          mesa_fdimeasurement.fdi_rgb, 
          mesa_fdipoint.point, 
          mesa_fdipoint.lon, 
          mesa_fdipoint.lat, 
          mesa_fdimeasurement.rain_mm, 
          mesa_fdimeasurement.windspd_kmh, 
          mesa_fdimeasurement.winddir_deg, 
          mesa_fdimeasurement.rh_pct, 
          mesa_fdimeasurement.temp_c, 
          mesa_fdimeasurement.date_time,
          FALSE AS is_forecast
FROM 
  public.mesa_fdipoint 
  LEFT JOIN public.mesa_fdimeasurement ON mesa_fdimeasurement.fdi_point_id = mesa_fdipoint.id

UNION

SELECT
          mesa_fdipoint.id, 
          mesa_fdipoint.name, 
          mesa_fdipoint.type, 
          mesa_fdipoint.station_name, 
          mesa_fdiforecast.fdi_value, 
          mesa_fdiforecast.fdi_rgb, 
          mesa_fdipoint.point, 
          mesa_fdipoint.lon, 
          mesa_fdipoint.lat, 
          mesa_fdiforecast.rain_mm, 
          mesa_fdiforecast.windspd_kmh, 
          mesa_fdiforecast.winddir_deg, 
          mesa_fdiforecast.rh_pct, 
          mesa_fdiforecast.temp_c, 
          mesa_fdiforecast.date_time,
          TRUE AS is_forecast
FROM 
  public.mesa_fdipoint 
  LEFT JOIN public.mesa_fdiforecast ON mesa_fdiforecast.fdi_point_id = mesa_fdipoint.id



--SELECT * FROM   mesa_fdiforecast;