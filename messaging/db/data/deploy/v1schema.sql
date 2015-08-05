-- Deploy v1schema

BEGIN;

CREATE SCHEMA "1";

GRANT USAGE ON SCHEMA "1" TO PUBLIC;
ALTER DATABASE gis SET search_path = "1", "public";

COMMIT;
