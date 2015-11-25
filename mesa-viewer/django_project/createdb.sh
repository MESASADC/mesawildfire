#!/bin/bash
createdb afis_test
createlang plpgsql afis_test
psql afis_test < /usr/share/postgresql-8.3-postgis/lwpostgis.sql
psql afis_test < /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql 

