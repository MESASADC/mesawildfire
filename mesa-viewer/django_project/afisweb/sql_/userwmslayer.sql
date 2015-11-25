--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: userwmslayer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('userwmslayer_id_seq', 13, true);


--
-- Data for Name: userwmslayer; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY userwmslayer (id, wmslayer_id, user_id, is_visible, is_deleted, "order") FROM stdin;
2	14	2	t	f	1
3	15	2	t	f	2
4	21	1	t	t	0
5	22	1	t	t	1
8	23	1	t	t	2
6	14	1	t	f	1
10	5	1	t	f	0
13	11	2	t	f	0
11	6	1	t	f	0
7	15	1	t	f	0
\.


--
-- PostgreSQL database dump complete
--

