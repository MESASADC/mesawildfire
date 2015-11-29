--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: sensor; Type: TABLE; Schema: public; Owner: timlinux; Tablespace: 
--


INSERT INTO sensor (name, description, layer) VALUES ('MODIS', 'MODIS', 'openafis:MODIS Active Fires Archive');
INSERT INTO sensor (name, description, layer) VALUES ('MSG', 'MSG', 'openafis:MSG Active Fires Archive');
INSERT INTO sensor (name, description, layer) VALUES ('ASIA-MODIS', 'ASIA-MODIS', 'openafis:asia_af_modis_datetime');


