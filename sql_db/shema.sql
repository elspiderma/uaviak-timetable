--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2 (Debian 13.2-1.pgdg100+1)
-- Dumped by pg_dump version 13.2

-- Started on 2021-04-02 20:30:38 +04

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

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 16385)
-- Name: groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    number character varying(30) NOT NULL
);


--
-- TOC entry 201 (class 1259 OID 16388)
-- Name: lessons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lessons (
    id_timetable integer NOT NULL,
    number integer NOT NULL,
    subject character varying(100) NOT NULL,
    cabinet character varying(10) NOT NULL,
    types integer[] NOT NULL,
    id_group integer NOT NULL,
    id_teacher integer NOT NULL,
    id integer NOT NULL
);


--
-- TOC entry 202 (class 1259 OID 16394)
-- Name: teachers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teachers (
    id integer NOT NULL,
    short_name character varying(30) NOT NULL,
    full_name character varying(30) NOT NULL
);


--
-- TOC entry 203 (class 1259 OID 16397)
-- Name: timetables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timetables (
    id integer NOT NULL,
    additional_info text,
    date date NOT NULL,
    departament integer NOT NULL
);


--
-- TOC entry 2816 (class 2606 OID 16404)
-- Name: groups group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- TOC entry 2818 (class 2606 OID 16406)
-- Name: lessons lesson_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lesson_pkey PRIMARY KEY (id);


--
-- TOC entry 2820 (class 2606 OID 16408)
-- Name: teachers teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (id);


--
-- TOC entry 2822 (class 2606 OID 16410)
-- Name: timetables timetables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables
    ADD CONSTRAINT timetables_pkey PRIMARY KEY (id);


--
-- TOC entry 2823 (class 2606 OID 16411)
-- Name: lessons lesson_id_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lesson_id_group_fkey FOREIGN KEY (id_group) REFERENCES public.groups(id);


--
-- TOC entry 2824 (class 2606 OID 16416)
-- Name: lessons lesson_id_teacher_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lesson_id_teacher_fkey FOREIGN KEY (id_teacher) REFERENCES public.teachers(id);


--
-- TOC entry 2825 (class 2606 OID 16421)
-- Name: lessons lesson_id_timetable_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lesson_id_timetable_fkey FOREIGN KEY (id_timetable) REFERENCES public.timetables(id) NOT VALID;


-- Completed on 2021-04-02 20:30:39 +04

--
-- PostgreSQL database dump complete
--

