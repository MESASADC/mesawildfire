-- Revert af_modis

BEGIN;

DROP TABLE af_modis CASCADE;

COMMIT;
