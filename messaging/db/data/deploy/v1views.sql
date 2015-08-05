-- Deploy v1views

BEGIN;

create or replace view "1".fire as
select *
from fire.detection;

COMMIT;