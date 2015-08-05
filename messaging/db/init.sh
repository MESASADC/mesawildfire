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

sqitch add v1schema -n "Adding_v1_schema"
sudo rm -Rf deploy/v1schema.sql revert/v1schema.sql
sudo cp -rf data/deploy/v1schema.sql deploy/
sudo cp -rf data/revert/v1schema.sql revert/

sqitch add af_modis -n "Adding_af_modis"
sudo rm -Rf deploy/af_modis.sql revert/af_modis.sql
sudo cp -rf data/deploy/af_modis.sql deploy/
sudo cp -rf data/revert/af_modis.sql revert/

sqitch deploy
