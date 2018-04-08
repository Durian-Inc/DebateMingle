--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: 25cen
--

CREATE TABLE public.account (
    username character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.account OWNER TO "25cen";

--
-- Name: topic; Type: TABLE; Schema: public; Owner: 25cen
--

CREATE TABLE public.topic (
    name character varying(80) NOT NULL
);


ALTER TABLE public.topic OWNER TO "25cen";

--
-- Name: votedon; Type: TABLE; Schema: public; Owner: 25cen
--

CREATE TABLE public.votedon (
    person character varying NOT NULL,
    topic character varying NOT NULL,
    vote integer NOT NULL
);


ALTER TABLE public.votedon OWNER TO "25cen";

--
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: 25cen
--

COPY public.account (username, password) FROM stdin;
innocent	b9316765c6ae419cfeb3f5af5517430e21e157c6c8bdca34446c6acf62655dd5
claymav	1b772db4b2c14b2310e45cd3963bac03f292c01dccc7b3e323ba199e3b3a8e14
griffin	8bb8daf7ba7fd71184cddecc0cebd6b6ace0cff967b193654c4556acb7778bfb
\.


--
-- Data for Name: topic; Type: TABLE DATA; Schema: public; Owner: 25cen
--

COPY public.topic (name) FROM stdin;
dogs
cats
Bees
skaters
Haters
\.


--
-- Data for Name: votedon; Type: TABLE DATA; Schema: public; Owner: 25cen
--

COPY public.votedon (person, topic, vote) FROM stdin;
innocent	dogs	0
griffin	dogs	1
claymav	dogs	1
claymav	Bees	1
innocent	Bees	1
innocent	skaters	1
innocent	Haters	0
\.


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: 25cen
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (username);


--
-- Name: topic topic_pkey; Type: CONSTRAINT; Schema: public; Owner: 25cen
--

ALTER TABLE ONLY public.topic
    ADD CONSTRAINT topic_pkey PRIMARY KEY (name);


--
-- Name: votedon votedon_pkey; Type: CONSTRAINT; Schema: public; Owner: 25cen
--

ALTER TABLE ONLY public.votedon
    ADD CONSTRAINT votedon_pkey PRIMARY KEY (person, topic, vote);


--
-- Name: votedon votedon_person_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 25cen
--

ALTER TABLE ONLY public.votedon
    ADD CONSTRAINT votedon_person_fkey FOREIGN KEY (person) REFERENCES public.account(username);


--
-- Name: votedon votedon_topic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: 25cen
--

ALTER TABLE ONLY public.votedon
    ADD CONSTRAINT votedon_topic_fkey FOREIGN KEY (topic) REFERENCES public.topic(name);


--
-- PostgreSQL database dump complete
--

