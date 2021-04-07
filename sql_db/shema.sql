--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2 (Debian 13.2-1.pgdg100+1)
-- Dumped by pg_dump version 13.2

-- Started on 2021-04-07 13:30:03 +04

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

--
-- TOC entry 219 (class 1255 OID 18440)
-- Name: add_lesson(integer, integer, character varying, character varying, integer[], character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.add_lesson(p_id_timetable integer, p_number integer, p_subject character varying, p_cabinet character varying, p_types integer[], p_group_number character varying, p_teacher_name character varying) RETURNS TABLE(id integer, id_timetable integer, number integer, subject character varying, cabinet character varying, types integer[], id_group integer, id_teacher integer)
    LANGUAGE plpgsql
    AS $$
    DECLARE
        teacher_id integer;
        group_id integer;
    BEGIN
        SELECT teachers.id INTO teacher_id FROM teachers WHERE teachers.short_name = p_teacher_name;
        IF teacher_id IS NULL THEN
            INSERT INTO teachers(short_name) VALUES(p_teacher_name) RETURNING teachers.id INTO teacher_id;
        END IF;

        SELECT groups.id INTO group_id FROM groups WHERE groups.number = p_group_number;
        IF group_id IS NULL THEN
            INSERT INTO groups(number) VALUES(p_group_number) RETURNING groups.id INTO group_id;
        END IF;

        RETURN QUERY
            INSERT INTO
                lessons(id_timetable, number, subject, cabinet, types, id_group, id_teacher)
            VALUES
                (p_id_timetable, p_number, p_subject, p_cabinet, p_types, group_id, teacher_id)
            RETURNING *;
    END;
$$;


SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 18003)
-- Name: groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    number character varying(30) NOT NULL
);


--
-- TOC entry 201 (class 1259 OID 18006)
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2980 (class 0 OID 0)
-- Dependencies: 201
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- TOC entry 202 (class 1259 OID 18008)
-- Name: lessons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lessons (
    id integer NOT NULL,
    id_timetable integer NOT NULL,
    number integer NOT NULL,
    subject character varying(100) NOT NULL,
    cabinet character varying(10) NOT NULL,
    types integer[] NOT NULL,
    id_group integer NOT NULL,
    id_teacher integer NOT NULL
);


--
-- TOC entry 203 (class 1259 OID 18014)
-- Name: lessons_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lessons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2981 (class 0 OID 0)
-- Dependencies: 203
-- Name: lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lessons_id_seq OWNED BY public.lessons.id;


--
-- TOC entry 204 (class 1259 OID 18016)
-- Name: teachers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teachers (
    id integer NOT NULL,
    short_name character varying(30) NOT NULL,
    full_name character varying(30)
);


--
-- TOC entry 205 (class 1259 OID 18019)
-- Name: teachers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.teachers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2982 (class 0 OID 0)
-- Dependencies: 205
-- Name: teachers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.teachers_id_seq OWNED BY public.teachers.id;


--
-- TOC entry 206 (class 1259 OID 18021)
-- Name: timetables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timetables (
    id integer NOT NULL,
    additional_info text,
    date date NOT NULL,
    departament integer NOT NULL
);


--
-- TOC entry 207 (class 1259 OID 18027)
-- Name: timetables_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.timetables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2983 (class 0 OID 0)
-- Dependencies: 207
-- Name: timetables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timetables_id_seq OWNED BY public.timetables.id;


--
-- TOC entry 2824 (class 2604 OID 18029)
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- TOC entry 2825 (class 2604 OID 18030)
-- Name: lessons id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons ALTER COLUMN id SET DEFAULT nextval('public.lessons_id_seq'::regclass);


--
-- TOC entry 2826 (class 2604 OID 18031)
-- Name: teachers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers ALTER COLUMN id SET DEFAULT nextval('public.teachers_id_seq'::regclass);


--
-- TOC entry 2827 (class 2604 OID 18032)
-- Name: timetables id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables ALTER COLUMN id SET DEFAULT nextval('public.timetables_id_seq'::regclass);


--
-- TOC entry 2829 (class 2606 OID 18292)
-- Name: groups groups_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_number_key UNIQUE (number);


--
-- TOC entry 2831 (class 2606 OID 18034)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2833 (class 2606 OID 18036)
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- TOC entry 2835 (class 2606 OID 18038)
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);


--
-- TOC entry 2837 (class 2606 OID 18290)
-- Name: teachers teachers_short_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_short_name_key UNIQUE (short_name);


--
-- TOC entry 2839 (class 2606 OID 18040)
-- Name: timetables timetables_departament_date_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables
    ADD CONSTRAINT timetables_departament_date_key UNIQUE (departament, date);


--
-- TOC entry 2841 (class 2606 OID 18042)
-- Name: timetables timetables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables
    ADD CONSTRAINT timetables_pkey PRIMARY KEY (id);


--
-- TOC entry 2843 (class 2606 OID 18298)
-- Name: lessons lessons_id_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_id_group_fkey FOREIGN KEY (id_group) REFERENCES public.groups(id) NOT VALID;


--
-- TOC entry 2844 (class 2606 OID 18303)
-- Name: lessons lessons_id_teacher_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_id_teacher_fkey FOREIGN KEY (id_teacher) REFERENCES public.teachers(id) NOT VALID;


--
-- TOC entry 2842 (class 2606 OID 18293)
-- Name: lessons lessons_id_timetable_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_id_timetable_fkey FOREIGN KEY (id_timetable) REFERENCES public.timetables(id) NOT VALID;


-- Completed on 2021-04-07 13:30:03 +04

--
-- PostgreSQL database dump complete
--

