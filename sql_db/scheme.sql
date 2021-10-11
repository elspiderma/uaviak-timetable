--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

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
-- Name: Departaments; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."Departaments" AS ENUM (
    'full_time',
    'correspondence'
);


--
-- Name: TypesLesson; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."TypesLesson" AS ENUM (
    'split',
    'practical',
    'consultation',
    'exam'
);


--
-- Name: add_lesson(integer, integer, character varying, character varying, public."TypesLesson"[], character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.add_lesson(p_id_timetable integer, p_number integer, p_subject character varying, p_cabinet character varying, p_types public."TypesLesson"[], p_group_number character varying, p_teacher_name character varying) RETURNS TABLE(id integer, id_timetable integer, number integer, subject character varying, cabinet character varying, types public."TypesLesson"[], id_group integer, id_teacher integer)
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


--
-- Name: add_or_update_vk_cache(character varying, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE public.add_or_update_vk_cache(p_key character varying, p_photo_id character varying)
    LANGUAGE plpgsql
    AS $$
    DECLARE
        v_count_cache_record int;
    BEGIN
        SELECT COUNT(*) INTO v_count_cache_record FROM vk_cache_photo WHERE key_cache = p_key;
        IF v_count_cache_record = 0 THEN
            INSERT INTO vk_cache_photo(key_cache, vk_photo_id) VALUES (p_key, p_photo_id);
        ELSE
            UPDATE vk_cache_photo SET vk_photo_id = p_photo_id WHERE key_cache = p_key;
        END IF;
    END;
    $$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chats; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chats (
    id integer NOT NULL,
    vk_id integer,
    timetable_photo boolean DEFAULT true
);


--
-- Name: chats_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chats_id_seq OWNED BY public.chats.id;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    number character varying(30) NOT NULL
);


--
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
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- Name: lessons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lessons (
    id integer NOT NULL,
    id_timetable integer NOT NULL,
    number integer NOT NULL,
    subject character varying(100) NOT NULL,
    cabinet character varying(10),
    types public."TypesLesson"[] NOT NULL,
    id_group integer NOT NULL,
    id_teacher integer NOT NULL
);


--
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
-- Name: lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lessons_id_seq OWNED BY public.lessons.id;


--
-- Name: subscriber_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscriber_group (
    id_user integer NOT NULL,
    id_group integer NOT NULL
);


--
-- Name: subscriber_teacher; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscriber_teacher (
    id_chat integer NOT NULL,
    id_teacher integer NOT NULL
);


--
-- Name: teachers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teachers (
    id integer NOT NULL,
    short_name character varying(30) NOT NULL,
    full_name character varying(30)
);


--
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
-- Name: teachers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.teachers_id_seq OWNED BY public.teachers.id;


--
-- Name: timetables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.timetables (
    id integer NOT NULL,
    additional_info text,
    date date NOT NULL,
    departament public."Departaments" NOT NULL
);


--
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
-- Name: timetables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.timetables_id_seq OWNED BY public.timetables.id;


--
-- Name: vk_cache_photo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vk_cache_photo (
    id integer NOT NULL,
    key_cache character varying(255),
    vk_photo_id character varying(100)
);


--
-- Name: vk_cache_photo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vk_cache_photo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vk_cache_photo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vk_cache_photo_id_seq OWNED BY public.vk_cache_photo.id;


--
-- Name: chats id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chats ALTER COLUMN id SET DEFAULT nextval('public.chats_id_seq'::regclass);


--
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- Name: lessons id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons ALTER COLUMN id SET DEFAULT nextval('public.lessons_id_seq'::regclass);


--
-- Name: teachers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers ALTER COLUMN id SET DEFAULT nextval('public.teachers_id_seq'::regclass);


--
-- Name: timetables id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables ALTER COLUMN id SET DEFAULT nextval('public.timetables_id_seq'::regclass);


--
-- Name: vk_cache_photo id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vk_cache_photo ALTER COLUMN id SET DEFAULT nextval('public.vk_cache_photo_id_seq'::regclass);


--
-- Name: chats chats_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chats
    ADD CONSTRAINT chats_pk PRIMARY KEY (id);


--
-- Name: groups groups_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_number_key UNIQUE (number);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- Name: subscriber_group subscriber_group_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber_group
    ADD CONSTRAINT subscriber_group_pk PRIMARY KEY (id_user, id_group);


--
-- Name: subscriber_teacher subscriber_teacher_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber_teacher
    ADD CONSTRAINT subscriber_teacher_pk PRIMARY KEY (id_chat, id_teacher);


--
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);


--
-- Name: teachers teachers_short_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_short_name_key UNIQUE (short_name);


--
-- Name: timetables timetables_departament_date_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables
    ADD CONSTRAINT timetables_departament_date_key UNIQUE (departament, date);


--
-- Name: timetables timetables_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.timetables
    ADD CONSTRAINT timetables_pkey PRIMARY KEY (id);


--
-- Name: chats_vk_user_id_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX chats_vk_user_id_uindex ON public.chats USING btree (vk_id);


--
-- Name: vk_cache_photo_key_cache_uindex; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX vk_cache_photo_key_cache_uindex ON public.vk_cache_photo USING btree (key_cache);


--
-- Name: lessons lessons_id_group_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_id_group_fkey FOREIGN KEY (id_group) REFERENCES public.groups(id) NOT VALID;


--
-- Name: lessons lessons_id_teacher_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_id_teacher_fkey FOREIGN KEY (id_teacher) REFERENCES public.teachers(id) NOT VALID;


--
-- Name: lessons lessons_id_timetable_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_id_timetable_fkey FOREIGN KEY (id_timetable) REFERENCES public.timetables(id) NOT VALID;


--
-- Name: subscriber_group subscriber_group_chats_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber_group
    ADD CONSTRAINT subscriber_group_chats_id_fk FOREIGN KEY (id_user) REFERENCES public.chats(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: subscriber_group subscriber_group_groups_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber_group
    ADD CONSTRAINT subscriber_group_groups_id_fk FOREIGN KEY (id_group) REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: subscriber_teacher subscriber_teacher_chats_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber_teacher
    ADD CONSTRAINT subscriber_teacher_chats_id_fk FOREIGN KEY (id_chat) REFERENCES public.chats(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: subscriber_teacher subscriber_teacher_teachers_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscriber_teacher
    ADD CONSTRAINT subscriber_teacher_teachers_id_fk FOREIGN KEY (id_teacher) REFERENCES public.teachers(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

