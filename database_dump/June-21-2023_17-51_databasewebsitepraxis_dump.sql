PGDMP     8    4                {            databasewebsitepraxis    15.2    15.2 	    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    17630    databasewebsitepraxis    DATABASE     �   CREATE DATABASE databasewebsitepraxis WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
 %   DROP DATABASE databasewebsitepraxis;
                WebsitePraxisServer    false            �            1259    17636    account_data    TABLE     _  CREATE TABLE public.account_data (
    account_uuid uuid NOT NULL,
    account_name text NOT NULL,
    account_password text NOT NULL,
    account_email text,
    account_address text,
    account_education text,
    account_phone_number text,
    account_email_verified boolean NOT NULL,
    account_creation_timestamp timestamp without time zone
);
     DROP TABLE public.account_data;
       public         heap    WebsitePraxisServer    false            �            1259    17631    account_login_session    TABLE       CREATE TABLE public.account_login_session (
    account_uuid uuid NOT NULL,
    login_session_uuid uuid NOT NULL,
    session_start_timestamp timestamp without time zone NOT NULL,
    last_refresh_timestamp timestamp without time zone NOT NULL,
    user_session_token text NOT NULL
);
 )   DROP TABLE public.account_login_session;
       public         heap    WebsitePraxisServer    false            �          0    17636    account_data 
   TABLE DATA           �   COPY public.account_data (account_uuid, account_name, account_password, account_email, account_address, account_education, account_phone_number, account_email_verified, account_creation_timestamp) FROM stdin;
    public          WebsitePraxisServer    false    215   �       �          0    17631    account_login_session 
   TABLE DATA           �   COPY public.account_login_session (account_uuid, login_session_uuid, session_start_timestamp, last_refresh_timestamp, user_session_token) FROM stdin;
    public          WebsitePraxisServer    false    214   �       i           2606    17642 *   account_data account_data_account_uuid_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.account_data
    ADD CONSTRAINT account_data_account_uuid_key UNIQUE (account_uuid);
 T   ALTER TABLE ONLY public.account_data DROP CONSTRAINT account_data_account_uuid_key;
       public            WebsitePraxisServer    false    215            �      x������ � �      �      x������ � �     