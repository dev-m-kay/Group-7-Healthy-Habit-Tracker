CREATE SCHEMA IF NOT EXISTS habits;

CREATE TABLE IF NOT EXISTS habits.user_detail (
    user_detail_id SERIAL NOT NULL,
    user_detail_username VARCHAR(50) NOT NULL,
    user_detail_password VARCHAR(255) NOT NULL,
    CONSTRAINT user_detail_pkey PRIMARY KEY (user_detail_id),
    CONSTRAINT user_detail_username_uq UNIQUE (user_detail_username)
);

CREATE TABLE IF NOT EXISTS habits.weight (
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

CREATE TABLE IF NOT EXISTS habits.workout (
    workout_id SERIAL NOT NULL,
    workout_name VARCHAR(50) NOT NULL,
    workout_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    workout_duration INT NOT NULL,
    workout_intensity INT NOT NULL,
    workout_type VARCHAR(50) NOT NULL,
    workout_log TEXT,
    workout_rating INT NOT NULL CHECK (
        workout_rating >= 1
        AND workout_rating <= 10
    ),
    user_detail_id INT NOT NULL,
    CONSTRAINT workout_pkey PRIMARY KEY (workout_id),
    CONSTRAINT workout_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS habits.diet (
    diet_id SERIAL NOT NULL,
    diet_name VARCHAR(50) NOT NULL,
    diet_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    diet_log TEXT,
    diet_rating INT NOT NULL CHECK (
        diet_rating >= 1
        AND diet_rating <= 10
    ),
    user_detail_id INT NOT NULL,
    CONSTRAINT diet_pkey PRIMARY KEY (diet_id),
    CONSTRAINT diet_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS habits.sleep (
    sleep_id SERIAL NOT NULL,
    sleep_duration DECIMAL NOT NULL,
    sleep_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sleep_log TEXT,
    sleep_rating INT NOT NULL CHECK (
        sleep_rating >= 1
        AND sleep_rating <= 10
    ),
    user_detail_id INT NOT NULL,
    CONSTRAINT sleep_pkey PRIMARY KEY (sleep_id),
    CONSTRAINT sleep_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS habits.goals(
    goal_id SERIAL NOT NULL,
    sleep_len_goal DECIMAL NOT NULL,
    better_sleep INT NOT NULL CHECK (
        better_sleep >= 1
            AND better_sleep <= 10
        ),
    intensity INT NOT NULL CHECK (
        intensity >= 1
        AND intensity  <= 10
        ),
    diet INT NOT NULL CHECK(
        diet >= 1
        AND diet <= 10
        ),
    user_detail_id INT NOT NULL UNIQUE,
    CONSTRAINT goals_pkey PRIMARY KEY (goal_id),
    CONSTRAINT goals_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE

);

CREATE TABLE habits.feedback (
    feedback_id SERIAL NOT NULL,
    feedback_type VARCHAR(50) NOT NULL,
    feedback_page VARCHAR(50) NOT NULL,
    feedback_message TEXT NOT NULL,
    feedback_rating INT CHECK (
        feedback_rating >= 1
        AND feedback_rating <= 5
    ),
    contact_email VARCHAR(120),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_detail_id INT NOT NULL,
    CONSTRAINT feedback_pkey PRIMARY KEY (feedback_id),
    CONSTRAINT feedback_user_detail_id_fkey FOREIGN KEY (user_detail_id) REFERENCES habits.user_detail (user_detail_id) ON DELETE CASCADE
);

