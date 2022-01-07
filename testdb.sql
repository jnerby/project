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
4	3	1	f
\.


--
-- Data for Name: clubs; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.clubs (club_id, name, owner_id) FROM stdin;
1	DragonWatch	1
2	Crow Fans	2
\.


--
-- Data for Name: films; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.films (film_id, club_id, tmdb_id, date_added, added_by, view_schedule, watched) FROM stdin;
5	1	415	2022-01-06 15:45:20.6114	1	\N	f
9	2	674	2022-01-06 15:46:21.86935	2	\N	f
12	2	12444	2022-01-06 15:46:26.821508	2	\N	f
6	2	671	2022-01-06 15:46:17.744988	2	2022-01-20 00:00:00	f
8	2	673	2022-01-06 15:46:20.80233	2	2022-01-15 00:00:00	f
11	2	672	2022-01-06 15:46:24.999532	2	2022-01-11 00:00:00	f
7	2	899082	2022-01-06 15:46:19.036756	2	\N	t
10	2	767	2022-01-06 15:46:23.940117	2	\N	t
13	1	109445	2022-01-06 15:47:47.96073	1	\N	f
14	1	44363	2022-01-06 15:47:52.791825	1	\N	f
4	1	364	2022-01-06 15:45:18.213783	1	2022-01-12 00:00:00	f
2	1	268	2022-01-06 15:45:15.28727	1	2022-01-15 00:00:00	f
1	1	414906	2022-01-06 15:45:14.31894	1	\N	t
3	1	272	2022-01-06 15:45:16.886381	1	\N	t
\.


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.ratings (rating_id, user_id, film_id, rating) FROM stdin;
1	2	7	9
2	2	10	7
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.users (user_id, fname, lname, email, phone, notifications, username, password_hash) FROM stdin;
1	Danaerys	Targaryen	dt@gmail.com	1234567890	f	dragonmum	pbkdf2:sha256:260000$giF5tb4Br3viS40v$3e192a41bd341b8561f302f6b19a7dee36a55c88f17cb1038a756a793238d570
2	Jon	Snow	js@gmail.com	1234567890	t	crowboy	pbkdf2:sha256:260000$BtYWLR6luw002GWL$f20bebe248196f99e1537bc341d15e69dfb743ce09a55aec7b16e6e80c63cf04
3	Khal	Drogo	kd@gmail.com	1234567890	f	khalD	pbkdf2:sha256:260000$j9ZAXsP0896cirgi$30b1cda494f9ce103c7c745415c4e238ed060808c9bd6e78ab9a54729c5466d4
4	Test	Test	test	0123456789	f	testuser	pbkdf2:sha256:260000$ZApDfQGqiX9zt5Rw$5380c975f994bd836e7a8e442257124c376ea0b78506d376e0bf02e6ca8232a5
\.


--
-- Name: club_users_club_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.club_users_club_user_id_seq', 4, true);


--
-- Name: clubs_club_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.clubs_club_id_seq', 2, true);


--
-- Name: films_film_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.films_film_id_seq', 14, true);


--
-- Name: ratings_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.ratings_rating_id_seq', 2, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.users_user_id_seq', 4, true);


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

