<<<<<<< HEAD
CREATE SCHEMA IF NOT EXISTS habits;

CREATE TABLE IF NOT EXISTS habits.user_detail (
=======
# Create the database
CREATE SCHEMA IF NOT EXISTS habits;

CREATE TABLE habits.user_detail (
>>>>>>> 447958f9fffb302a145f52b0d5b28564adb8a5cb
    user_detail_id SERIAL NOT NULL,
    user_detail_username VARCHAR(50) NOT NULL,
    user_detail_password VARCHAR(255) NOT NULL,
    CONSTRAINT user_detail_pkey PRIMARY KEY (user_detail_id),
    CONSTRAINT user_detail_username_uq UNIQUE (user_detail_username)
);

<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS habits.weight (
=======
CREATE TABLE habits.weight (
>>>>>>> 447958f9fffb302a145f52b0d5b28564adb8a5cb
    weight_id SERIAL NOT NULL,
    weight_value INT NOT NULL CHECK (
        weight_value >= 0
        AND weight_value <= 999
    ),
    weight_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_detail_id INT NOT NULL,
    CONSTRAINT weight_pkey PRIMARY KEY (weight_id),
    CONSTRAINT weight_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);

<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS habits.workout (
=======
CREATE TABLE habits.workout (
>>>>>>> 447958f9fffb302a145f52b0d5b28564adb8a5cb
    workout_id SERIAL NOT NULL,
    workout_name VARCHAR(50) NOT NULL,
    workout_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    workout_duration INT NOT NULL,
    workout_intensity INT NOT NULL,
    workout_type VARCHAR(50) NOT NULL,
    user_detail_id INT NOT NULL,
    CONSTRAINT workout_pkey PRIMARY KEY (workout_id),
    CONSTRAINT workout_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);

<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS habits.diet (
=======
CREATE TABLE habits.diet (
>>>>>>> 447958f9fffb302a145f52b0d5b28564adb8a5cb
    diet_id SERIAL NOT NULL,
    diet_name VARCHAR(50) NOT NULL,
    diet_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    diet_rating INT NOT NULL CHECK (
        diet_rating >= 1
        AND diet_rating <= 10
    ),
    user_detail_id INT NOT NULL,
    CONSTRAINT diet_pkey PRIMARY KEY (diet_id),
    CONSTRAINT diet_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);

<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS habits.sleep (
=======
CREATE TABLE habits.sleep (
>>>>>>> 447958f9fffb302a145f52b0d5b28564adb8a5cb
    sleep_id SERIAL NOT NULL,
    sleep_duration INT NOT NULL,
    sleep_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sleep_rating INT NOT NULL CHECK (
        sleep_rating >= 1
        AND sleep_rating <= 10
    ),
    user_detail_id INT NOT NULL,
    CONSTRAINT sleep_pkey PRIMARY KEY (sleep_id),
    CONSTRAINT sleep_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);