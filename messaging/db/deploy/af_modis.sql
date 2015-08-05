-- Deploy af_modis

BEGIN;

CREATE TABLE "1".af_modis  
(
  pk serial PRIMARY KEY,
  type text NOT NULL,
  geom point NOT NULL,
  lat decimal NOT NULL,
  lon decimal NOT NULL,
  date_time timestamp without time zone NOT NULL,
  src text NOT NULL,
  btemp decimal NOT NULL,
  sat text NOT NULL,
  frp decimal NOT NULL
);

CREATE OR REPLACE VIEW "1".modis_af AS

SELECT *
FROM af_modis;


COMMIT;
