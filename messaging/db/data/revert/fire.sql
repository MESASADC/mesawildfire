-- Revert fire

BEGIN;

DROP TABLE film.detection CASCADE;

COMMIT;