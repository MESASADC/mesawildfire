#! /bin/bash

set -x
source ENV
postgrest  --db-host $POSTGREST_DB_HOST           --db-port $POSTGREST_DB_PORT \
               --db-name $POSTGREST_DB_NAME       --db-user $POSTGREST_DB_USER \
               --db-pass $POSTGREST_DB_PASS       --db-pool $POSTGREST_DB_POOL \
               --anonymous $POSTGREST_DB_ANONYMOUS --port $POSTGREST_PORT        \
               --v1schema public