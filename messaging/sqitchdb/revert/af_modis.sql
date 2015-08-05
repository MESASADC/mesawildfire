-- Revert af_modis

BEGIN;

DROP TABLE public.af_modis CASCADE;

COMMIT;
