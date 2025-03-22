-- Utility scripts for cleaning up data
WITH RECURSIVE
    split_actors (rowid, actor, remaining) AS (
        SELECT
            rowid,
            trim(
                substr (
                    leading_actors || ',',
                    1,
                    instr (leading_actors || ',', ',') - 1
                )
            ) AS actor,
            substr (
                leading_actors || ',',
                instr (leading_actors || ',', ',') + 1
            ) AS remaining
        FROM
            movies
        UNION ALL
        SELECT
            rowid,
            trim(substr (remaining, 1, instr (remaining, ',') - 1)) AS actor,
            substr (remaining, instr (remaining, ',') + 1) AS remaining
        FROM
            split_actors
        WHERE
            remaining <> ''
    )
INSERT INTO
    actor (name)
SELECT DISTINCT
    actor
FROM
    split_actors
WHERE
    actor <> '';

BEGIN TRANSACTION;

UPDATE movies
SET
    title = 'The ' || substr (title, 1, length (title) - 5)
WHERE
    title LIKE '%, The';

UPDATE movies
SET
    sort_title = CASE
        WHEN title LIKE 'The %' THEN substr (title, 5)
        ELSE title
    END;

COMMIT;

WITH RECURSIVE
    split_actors (movie_id, actor, remaining) AS (
        SELECT
            id AS movie_id,
            trim(
                substr (
                    leading_actors || ',',
                    1,
                    instr (leading_actors || ',', ',') - 1
                )
            ) AS actor,
            substr (
                leading_actors || ',',
                instr (leading_actors || ',', ',') + 1
            ) AS remaining
        FROM
            movies
        UNION ALL
        SELECT
            movie_id,
            trim(substr (remaining, 1, instr (remaining, ',') - 1)) AS actor,
            substr (remaining, instr (remaining, ',') + 1) AS remaining
        FROM
            split_actors
        WHERE
            remaining <> ''
    )
INSERT INTO
    actor_movie_reference (movie_id, actor_id)
SELECT
    movie_id,
    a.id
FROM
    split_actors
    JOIN actor a ON a.name = split_actors.actor
WHERE
    split_actors.actor <> '';