--
-- PostgreSQL database cluster dump
--

-- Started on 2023-06-18 18:14:31

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE "WebsitePraxisServer";
ALTER ROLE "WebsitePraxisServer" WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:GsTiHglLGSyw2GtlQvvcRQ==$21tjmBDXFmgmwLMp2gidkkmK71JgqFvy0iEzUowexeU=:nPBnMsDdWImQTb6Fe3sAhjw2wk4sx/dNBl1zQheVP6M=';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:O1CWdFKYT9miBnyR23+K1A==$qcO+hhKJwngzoGS7d0UiMLDAN5ZX+vRZwMTb3yRxFlE=:K519olFyv8Wlr6RmtT6gGBkHtby9F8K+HJpj65i82+w=';

--
-- User Configurations
--








-- Completed on 2023-06-18 18:14:31

--
-- PostgreSQL database cluster dump complete
--

