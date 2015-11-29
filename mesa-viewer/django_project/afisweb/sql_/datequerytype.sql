--
-- PostgreSQL database dump
--

-- Started on 2010-01-01 17:26:29

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 2643 (class 0 OID 0)
-- Dependencies: 2333
-- Name: datequerytype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('datequerytype_id_seq', 3, true);


--
-- TOC entry 2640 (class 0 OID 26467)
-- Dependencies: 2334
-- Data for Name: datequerytype; Type: TABLE DATA; Schema: public; Owner: timlinux
--

INSERT INTO datequerytype (id, name, hours) VALUES (1, 'Last 24 hours', 24);
INSERT INTO datequerytype (id, name, hours) VALUES (2, 'Last 48 hours', 48);
INSERT INTO datequerytype (id, name, hours) VALUES (3, 'Last week', 168);


-- Completed on 2010-01-01 17:26:29

--
-- PostgreSQL database dump complete
--

