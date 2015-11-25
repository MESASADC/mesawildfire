#!/bin/bash
# This script creates a database role "afisviewer" with a schema search path that allows the viewer, alerts, query
# interface and other apps to share the same django auth tables. This was done as a type of "single-signon" or 
# at least shared credentials solution.
psql -c "CREATE ROLE afisviewer LOGIN NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;" afisapps postgres
psql -c "ALTER ROLE afisviewer SET search_path=viewer, common, postgis;" afisapps postgres
