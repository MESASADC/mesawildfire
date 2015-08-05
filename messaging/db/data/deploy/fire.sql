- Deploy fire

BEGIN;

CREATE TABLE fire.detection  
(
  pk serial PRIMARY KEY,
  type text NOT NULL,
  geom point NOT NULL,
  lat decimal NOT NULL,
  lon decimal NOT NULL,
  date_time timestamp without timezone NOT NULL,
  src text NOT NULL,
  btemp decimal NOT NULL,
  sat text NOT NULL,
  frp decimal NOT NULL
);

COMMIT;
