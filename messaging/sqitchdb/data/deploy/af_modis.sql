-- Deploy af_modis

BEGIN;

CREATE TABLE public.af_modis
(
  pk SERIAL PRIMARY KEY,
  type TEXT NOT NULL,
  geom POINT,
  lat DECIMAL NOT NULL,
  lon DECIMAL NOT NULL,
  date_time TIMESTAMP WITHOUT TIME ZONE,
  src TEXT NOT NULL,
  btemp DECIMAL NOT NULL,
  sat TEXT NOT NULL,
  frp DECIMAL NOT NULL
);

CREATE OR REPLACE VIEW "1".active_fire_modis AS
SELECT * FROM public.af_modis;

COMMIT;

