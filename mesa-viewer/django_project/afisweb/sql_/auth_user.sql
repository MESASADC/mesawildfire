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
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('auth_user_id_seq', 2, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
2	anonymous				sha1$3e8c5$c66c356ebc2bc470f7ede7f48e2bf6b793fdd500	f	t	f	2010-03-12 10:24:49+02	2010-03-12 10:24:49+02
1	timlinux			tim@linfiniti.com	sha1$9a2e8$d30797c33649f9720e8ece7c07c4b2bb4b821427	t	t	t	2010-04-04 00:07:03.016406+02	2010-02-26 14:49:19.505714+02
\.


--
-- PostgreSQL database dump complete
--

