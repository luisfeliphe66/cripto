CREATE DATABASE IF NOT EXISTS BTC;

ALTER SCHEMA `BTC`  DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_general_ci ;
USE BTC;

CREATE TABLE BTCBRL (
    code VARCHAR(255),
    codein VARCHAR(255),
    name VARCHAR(255),
    high VARCHAR(255),
    low VARCHAR(255),
    varBid VARCHAR(255),
    pctChange VARCHAR(255),
    bid VARCHAR(255),
    ask VARCHAR(255),
    timestamp INT,
    create_date DATETIME,
    PRIMARY KEY (code)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;