#! /bin/bash

set -x
rm -Rf deploy revert verify sqitch.conf sqitch.plan
source ENV

sqitch init $SQITCH_PROJECT_NAME
sqitch config core.engine pg
sqitch config --user user.name $SQITCH_NAME
sqitch config --user user.email $SQITCH_EMAIL
sqitch config --bool deploy.verify true
sqitch config --bool rebase.verify true

sqitch target add production \
 db:pg://$SQITCH_DB_USER:$SQITCH_DB_PASS@$SQITCH_DB_HOST:$SQITCH_DB_PORT/$SQITCH_DB_NAME
sqitch engine add pg
sqitch engine set-target pg production
#sqitch engine update-config

sqitch add appschema -n "Add_schema_for_$SQITCH_PROJECT_NAME"
sudo rm -Rf deploy/appschema.sql revert/appschema.sql
sudo cp -rf data/deploy/appschema.sql deploy/
sudo cp -rf data/revert/appschema.sql revert/

sqitch deploy

sqitch add fire -n "Add_table_for_fire"
sudo rm -Rf deploy/fire.sql revert/fire.sql
sudo cp -rf data/deploy/fire.sql deploy/
sudo cp -rf data/revert/fire.sql revert/

sqitch deploy


sqitch add v1schema -n "Adding_API_v1_schema"
sudo rm -Rf deploy/v1schema.sql revert/v1schema.sql
sudo cp -rf data/deploy/v1schema.sql deploy/
sudo cp -rf data/revert/v1schema.sql revert/

sqitch deploy

sqitch add v1views -n "Adding_API_v1_views"
sudo rm -Rf deploy/v1views.sql revert/v1views.sql
sudo cp -rf data/deploy/v1views.sql deploy/
sudo cp -rf data/revert/v1views.sql revert/

sqitch deploy