# Delete all tables and schema in the habits database for cleanup

DROP TABLE IF EXISTS habits.weight;

DROP TABLE IF EXISTS habits.workout;

DROP TABLE IF EXISTS habits.diet;

DROP TABLE IF EXISTS habits.sleep;

DROP TABLE IF EXISTS habits.user_detail;

DROP SCHEMA habits;