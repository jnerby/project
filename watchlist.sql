--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: club_users; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.club_users (
    club_user_id integer NOT NULL,
    user_id integer NOT NULL,
    club_id integer NOT NULL,
    approved boolean NOT NULL
);


ALTER TABLE public.club_users OWNER TO jnerby;

--
-- Name: club_users_club_user_id_seq; Type: SEQUENCE; Schema: public; Owner: jnerby
--

CREATE SEQUENCE public.club_users_club_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.club_users_club_user_id_seq OWNER TO jnerby;

--
-- Name: club_users_club_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jnerby
--

ALTER SEQUENCE public.club_users_club_user_id_seq OWNED BY public.club_users.club_user_id;


--
-- Name: clubs; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.clubs (
    club_id integer NOT NULL,
    name character varying(30),
    owner_id integer
);


ALTER TABLE public.clubs OWNER TO jnerby;

--
-- Name: clubs_club_id_seq; Type: SEQUENCE; Schema: public; Owner: jnerby
--

CREATE SEQUENCE public.clubs_club_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clubs_club_id_seq OWNER TO jnerby;

--
-- Name: clubs_club_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jnerby
--

ALTER SEQUENCE public.clubs_club_id_seq OWNED BY public.clubs.club_id;


--
-- Name: films; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.films (
    film_id integer NOT NULL,
    club_id integer NOT NULL,
    tmdb_id integer,
    date_added timestamp without time zone,
    added_by integer NOT NULL,
    view_schedule timestamp without time zone,
    watched boolean NOT NULL
);


ALTER TABLE public.films OWNER TO jnerby;

--
-- Name: films_film_id_seq; Type: SEQUENCE; Schema: public; Owner: jnerby
--

CREATE SEQUENCE public.films_film_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.films_film_id_seq OWNER TO jnerby;

--
-- Name: films_film_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jnerby
--

ALTER SEQUENCE public.films_film_id_seq OWNED BY public.films.film_id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.ratings (
    rating_id integer NOT NULL,
    user_id integer NOT NULL,
    film_id integer NOT NULL,
    rating integer NOT NULL
);


ALTER TABLE public.ratings OWNER TO jnerby;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: jnerby
--

CREATE SEQUENCE public.ratings_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ratings_rating_id_seq OWNER TO jnerby;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jnerby
--

ALTER SEQUENCE public.ratings_rating_id_seq OWNED BY public.ratings.rating_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    fname character varying(25),
    lname character varying(25),
    email character varying(30),
    phone character varying(10),
    notifications boolean NOT NULL,
    username character varying(25),
    password_hash character varying(128)
);


ALTER TABLE public.users OWNER TO jnerby;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: jnerby
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO jnerby;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jnerby
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: club_users club_user_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.club_users ALTER COLUMN club_user_id SET DEFAULT nextval('public.club_users_club_user_id_seq'::regclass);


--
-- Name: clubs club_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.clubs ALTER COLUMN club_id SET DEFAULT nextval('public.clubs_club_id_seq'::regclass);


--
-- Name: films film_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.films ALTER COLUMN film_id SET DEFAULT nextval('public.films_film_id_seq'::regclass);


--
-- Name: ratings rating_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.ratings ALTER COLUMN rating_id SET DEFAULT nextval('public.ratings_rating_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: club_users; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.club_users (club_user_id, user_id, club_id, approved) FROM stdin;
1	1	1	t
3	2	2	t
2	2	1	t
4	3	1	t
5	1	3	t
6	3	3	t
7	1	2	f
8	1	4	t
9	5	5	t
10	6	6	t
11	5	6	t
\.


--
-- Data for Name: clubs; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.clubs (club_id, name, owner_id) FROM stdin;
1	DragonWatch	1
2	Crow Fans	2
3	the_khalasar	1
4	NightsWatch	1
6	WolfWatch	6
5	underFoot	5
\.


--
-- Data for Name: films; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.films (film_id, club_id, tmdb_id, date_added, added_by, view_schedule, watched) FROM stdin;
7	2	899082	2022-01-06 15:46:19.036756	2	\N	t
10	2	767	2022-01-06 15:46:23.940117	2	\N	t
1	1	414906	2022-01-06 15:45:14.31894	1	\N	t
3	1	272	2022-01-06 15:45:16.886381	1	\N	t
2	1	268	2022-01-06 15:45:15.28727	1	2022-01-15 00:00:00	t
4	1	364	2022-01-06 15:45:18.213783	1	2022-01-12 00:00:00	t
5	1	415	2022-01-06 15:45:20.6114	1	\N	t
9	2	674	2022-01-06 15:46:21.86935	2	\N	t
12	2	12444	2022-01-06 15:46:26.821508	2	\N	t
16	1	671	2022-01-10 14:28:25.565445	1	2022-01-12 00:00:00	t
17	1	767	2022-01-10 14:28:26.679168	1	2022-01-22 00:00:00	t
18	1	672	2022-01-10 14:28:27.791977	1	2022-01-20 00:00:00	f
20	3	209112	2022-01-10 17:55:22.487998	1	2022-01-22 00:00:00	f
24	2	12445	2022-01-11 17:31:20.281131	2	\N	f
21	2	10719	2022-01-11 13:29:47.532685	2	2022-01-29 00:00:00	f
22	2	673	2022-01-11 17:31:17.034118	2	2022-01-22 00:00:00	f
23	2	675	2022-01-11 17:31:18.935816	2	2022-01-13 00:00:00	f
25	2	9479	2022-01-11 18:22:11.465022	2	\N	f
26	2	4011	2022-01-11 18:22:19.250282	2	\N	f
27	2	535470	2022-01-12 10:02:36.050423	2	2022-01-15 00:00:00	t
28	2	247706	2022-01-12 10:26:13.169002	2	\N	f
30	5	121	2022-01-12 12:30:40.757863	5	2022-01-15 00:00:00	f
32	5	566525	2022-01-12 12:49:50.969383	5	\N	f
31	5	120	2022-01-12 12:30:42.502375	5	2022-01-14 00:00:00	f
33	6	15257	2022-01-12 12:52:43.300148	6	\N	f
34	6	76170	2022-01-12 12:52:44.533227	6	\N	f
38	6	276148	2022-01-12 12:52:59.503462	6	\N	f
35	6	2080	2022-01-12 12:52:45.837749	6	2022-01-29 00:00:00	f
37	6	263115	2022-01-12 12:52:49.641906	6	2022-01-22 00:00:00	f
39	6	11824	2022-01-12 12:53:29.756209	6	2022-02-09 00:00:00	t
40	6	15582	2022-01-12 12:53:31.324822	6	2022-02-02 00:00:00	f
43	5	49636	2022-01-12 13:05:09.804445	5	\N	t
42	5	11841	2022-01-12 13:04:36.664243	5	\N	t
44	5	13481	2022-01-12 13:05:42.931531	5	\N	t
\.


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.ratings (rating_id, user_id, film_id, rating) FROM stdin;
1	2	7	9
2	2	10	7
3	1	1	9
4	1	3	9
5	1	4	8
6	1	5	8
7	2	12	10
8	2	9	8
9	1	16	9
10	1	2	1
11	6	39	10
12	5	43	9
13	5	42	10
14	5	44	9
15	5	39	5
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.users (user_id, fname, lname, email, phone, notifications, username, password_hash) FROM stdin;
3	Khal	Drogo	kd@gmail.com	1234567890	f	khalD	pbkdf2:sha256:260000$j9ZAXsP0896cirgi$30b1cda494f9ce103c7c745415c4e238ed060808c9bd6e78ab9a54729c5466d4
4	Test	Test	test	0123456789	f	testuser	pbkdf2:sha256:260000$ZApDfQGqiX9zt5Rw$5380c975f994bd836e7a8e442257124c376ea0b78506d376e0bf02e6ca8232a5
1	Danaerys	Targaryen	dt@gmail.com	1234567890	t	dragonmum	pbkdf2:sha256:260000$giF5tb4Br3viS40v$3e192a41bd341b8561f302f6b19a7dee36a55c88f17cb1038a756a793238d570
2	Jon	Snow	js@gmail.com	1234567890	f	crowboy	pbkdf2:sha256:260000$BtYWLR6luw002GWL$f20bebe248196f99e1537bc341d15e69dfb743ce09a55aec7b16e6e80c63cf04
5	Arya	Stark	as@gmail.com	1234567890	t	aGirlHasNoUsername	pbkdf2:sha256:260000$FN1rLXGE6tOnvCVq$081a571f2f56a9448930d050a3bb0f6c5ef4753cfbe8078ca6e60477d9ad6a85
6	Ned	Stark	ns@gmail.com	0123456789	t	neds_dead	pbkdf2:sha256:260000$zp45RhNQPSLuMZba$9800e4f233ba632a138ae63f07646295687b44513c58da7d2059d4cc25119f02
\.


--
-- Name: club_users_club_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.club_users_club_user_id_seq', 11, true);


--
-- Name: clubs_club_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.clubs_club_id_seq', 6, true);


--
-- Name: films_film_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.films_film_id_seq', 44, true);


--
-- Name: ratings_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.ratings_rating_id_seq', 15, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.users_user_id_seq', 6, true);


--
-- Name: club_users club_users_pkey; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.club_users
    ADD CONSTRAINT club_users_pkey PRIMARY KEY (club_user_id);


--
-- Name: clubs clubs_pkey; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.clubs
    ADD CONSTRAINT clubs_pkey PRIMARY KEY (club_id);


--
-- Name: films films_pkey; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.films
    ADD CONSTRAINT films_pkey PRIMARY KEY (film_id);


--
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (rating_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: club_users club_users_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.club_users
    ADD CONSTRAINT club_users_club_id_fkey FOREIGN KEY (club_id) REFERENCES public.clubs(club_id);


--
-- Name: club_users club_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.club_users
    ADD CONSTRAINT club_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: clubs clubs_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.clubs
    ADD CONSTRAINT clubs_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id);


--
-- Name: films films_added_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.films
    ADD CONSTRAINT films_added_by_fkey FOREIGN KEY (added_by) REFERENCES public.users(user_id);


--
-- Name: films films_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.films
    ADD CONSTRAINT films_club_id_fkey FOREIGN KEY (club_id) REFERENCES public.clubs(club_id);


--
-- Name: ratings ratings_film_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_film_id_fkey FOREIGN KEY (film_id) REFERENCES public.films(film_id);


--
-- Name: ratings ratings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

