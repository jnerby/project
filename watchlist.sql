--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

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
    added_by integer NOT NULL
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
-- Name: users; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    fname character varying(25),
    lname character varying(25),
    email character varying(30),
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
-- Name: votes; Type: TABLE; Schema: public; Owner: jnerby
--

CREATE TABLE public.votes (
    vote_id integer NOT NULL,
    user_id integer NOT NULL,
    film_id integer NOT NULL,
    vote boolean NOT NULL
);


ALTER TABLE public.votes OWNER TO jnerby;

--
-- Name: votes_vote_id_seq; Type: SEQUENCE; Schema: public; Owner: jnerby
--

CREATE SEQUENCE public.votes_vote_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.votes_vote_id_seq OWNER TO jnerby;

--
-- Name: votes_vote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jnerby
--

ALTER SEQUENCE public.votes_vote_id_seq OWNED BY public.votes.vote_id;


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
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: votes vote_id; Type: DEFAULT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.votes ALTER COLUMN vote_id SET DEFAULT nextval('public.votes_vote_id_seq'::regclass);


--
-- Data for Name: club_users; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.club_users (club_user_id, user_id, club_id, approved) FROM stdin;
1	1	22	f
2	1	23	f
3	1	24	f
4	1	25	f
5	1	26	t
6	1	27	t
\.


--
-- Data for Name: clubs; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.clubs (club_id, name, owner_id) FROM stdin;
1	Personal	1
2	Personal	1
3	Personal	1
4	Personal	1
5	Personal	1
6	Personal	1
7	Personal	1
8	test1	1
9	test1	1
10	Personal	1
11	Personal	1
12	Personal	1
13	test1	1
14	test2	1
15	test2	1
16	test2	1
17	test2	1
18	test1	1
19	test1	1
20	test1	1
21	Personal	1
22	Personal	1
23	test4	1
24	test4	1
25	Personal	1
26	Personal	1
27	My Group Club	1
\.


--
-- Data for Name: films; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.films (film_id, club_id, tmdb_id, date_added, added_by) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.users (user_id, fname, lname, email, username, password_hash) FROM stdin;
1	First	Last	Email	Username	pbkdf2:sha256:260000$iqq6GcQTMUVCmdJu$c52b3299b0ab6392ed2cb197616bfac8be4bbe19139140f29508cdbdb103b5c8
\.


--
-- Data for Name: votes; Type: TABLE DATA; Schema: public; Owner: jnerby
--

COPY public.votes (vote_id, user_id, film_id, vote) FROM stdin;
\.


--
-- Name: club_users_club_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.club_users_club_user_id_seq', 6, true);


--
-- Name: clubs_club_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.clubs_club_id_seq', 27, true);


--
-- Name: films_film_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.films_film_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: votes_vote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jnerby
--

SELECT pg_catalog.setval('public.votes_vote_id_seq', 1, false);


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
-- Name: votes votes_pkey; Type: CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_pkey PRIMARY KEY (vote_id);


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
-- Name: votes votes_film_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_film_id_fkey FOREIGN KEY (film_id) REFERENCES public.films(film_id);


--
-- Name: votes votes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jnerby
--

ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

