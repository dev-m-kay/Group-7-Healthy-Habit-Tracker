# Inserts data into the database
INSERT INTO habits.user_detail (user_detail_username, user_detail_password) VALUES
('john_doe', 'example123'),
('jane_doe', 'password456'),
('alice_smith', 'alicepass789'),
('bob_jones', 'bobsecure123');

INSERT INTO
    habits.weight (
        weight_value,
        weight_date,
        user_detail_id
    )
VALUES (220, '2023-10-01 08:00:00', 1),
    (130, '2023-10-02 08:00:00', 2),
    (125, '2023-10-03 08:00:00', 3),
    (280, '2023-10-04 08:00:00', 4);

INSERT INTO
    habits.workout (
        workout_name,
        workout_date,
        workout_duration,
        workout_intensity,
        workout_type,
        user_detail_id
    )
VALUES (
        'Morning Run',
        '2023-10-01 07:00:00',
        30,
        5,
        'Cardio',
        1
    ),
    (
        'Evening Yoga',
        '2023-10-02 18:00:00',
        45,
        3,
        'Abs',
        2
    ),
    (
        'Weightlifting',
        '2023-10-03 17:00:00',
        60,
        4,
        'Arms',
        3
    ),
    (
        'Weightlifting',
        '2023-10-04 16:00:00',
        90,
        6,
        'Legs',
        4
    );

INSERT INTO
    habits.diet (
        diet_name,
        diet_date,
        diet_rating,
        user_detail_id
    )
VALUES (
        'Pizza',
        '2023-10-01 12:00:00',
        8,
        1
    ),
    (
        'Steak',
        '2023-10-02 13:00:00',
        9,
        2
    ),
    (
        'Salad',
        '2023-10-03 14:00:00',
        7,
        3
    ),
    (
        'Chicken',
        '2023-10-04 15:00:00',
        10,
        4
    );

INSERT INTO
    habits.sleep (
        sleep_duration,
        sleep_date,
        sleep_rating,
        user_detail_id
    )
VALUES (
        8,
        '2023-10-01 22:00:00',
        8,
        1
    ),
    (
        9,
        '2023-10-02 23:00:00',
        7,
        2
    ),
    (
        6,
        '2023-10-03 21:00:00',
        6,
        3
    ),
    (
        7,
        '2023-10-04 20:00:00',
        9,
        4
    );