-- SET statement_timeout = 0;
-- SET lock_timeout = 0;
-- SET idle_in_transaction_session_timeout = 0;
\connect bitcoin;
SET client_encoding = 'UTF8';
-- SET standard_conforming_strings = on;
-- SELECT pg_catalog.set_config('search_path', '', false);
-- SET check_function_bodies = false;
-- SET client_min_messages = warning;
-- SET row_security = off;

-- CREATE DATABASE bitcoin;
CREATE TABLE timeseries(tsm INT NOT NULL PRIMARY KEY);
CREATE TABLE coinbase(tsm INT UNIQUE,
            price_open NUMERIC,
            price_high NUMERIC,
            price_low NUMERIC,
            price_close NUMERIC,
            volume_btc NUMERIC,
            volume_currency NUMERIC,
            weighted_price NUMERIC,
            CONSTRAINT fk_coin_tsm FOREIGN KEY (tsm) REFERENCES timeseries (tsm)
            );

CREATE TABLE bitbase(tsm INT UNIQUE references timeseries(tsm),
            price_open NUMERIC,
            price_high NUMERIC,
            price_low NUMERIC,
            price_close NUMERIC,
            volume_btc NUMERIC,
            volume_currency NUMERIC,
            weighted_price NUMERIC,
            CONSTRAINT fk_bit_tsm FOREIGN KEY (tsm) REFERENCES timeseries (tsm)
            );




CREATE TABLE redditsub(tsm INT references timeseries(tsm),
            body TEXT,
            score INT,
            author VARCHAR(255),
            CONSTRAINT fk_redditsub_tsm FOREIGN KEY (tsm) REFERENCES timeseries (tsm)
);