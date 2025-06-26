CREATE SCHEMA IF NOT EXISTS habits;

CREATE TABLE habits.user_detail (
    user_detail_id SERIAL NOT NULL,
    user_detail_username VARCHAR(50) NOT NULL,
    user_detail_password VARCHAR(255) NOT NULL,
    CONSTRAINT user_detail_pkey PRIMARY KEY (user_detail_id),
    CONSTRAINT user_detail_username_uq UNIQUE (user_detail_username)
);