--
-- PostgreSQL database dump
--

-- Started on 2009-12-26 18:04:21

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 2631 (class 0 OID 0)
-- Dependencies: 2320
-- Name: wmslayergroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('wmslayergroup_id_seq', 1, true);


--
-- TOC entry 2628 (class 0 OID 17955)
-- Dependencies: 2321
-- Data for Name: wmslayergroup; Type: TABLE DATA; Schema: public; Owner: timlinux
--

INSERT INTO wmslayergroup (id, name, owner_id) VALUES (1, 'Default Layers', 1);


-- Completed on 2009-12-26 18:04:21

--
-- PostgreSQL database dump complete
--

