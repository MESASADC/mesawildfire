-- Revert v1schema

BEGIN;

DROP SCHEMA "1";

ALTER DATABASE gis SET search_path = "public";

COMMIT;
