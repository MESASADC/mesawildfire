--
-- PostgreSQL database dump
--

-- Started on 2009-12-26 18:04:45

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 2629 (class 0 OID 0)
-- Dependencies: 2326
-- Name: imageformat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('imageformat_id_seq', 2, true);


--
-- TOC entry 2626 (class 0 OID 18025)
-- Dependencies: 2327
-- Data for Name: imageformat; Type: TABLE DATA; Schema: public; Owner: timlinux
--

INSERT INTO imageformat (id, name, mime_type) values (1,	'png',	'image/png');
INSERT INTO imageformat (id, name, mime_type) values (2,	'jpg',	'image/jpeg');


-- Completed on 2009-12-26 18:04:45

--
-- PostgreSQL database dump complete
--

