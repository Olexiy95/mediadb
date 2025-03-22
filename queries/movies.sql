-- name: get_all_movies
SELECT
    md.id as ID,
    md.title as Title,
    md.rating as Rating,
    mv.year as Year,
    g.name as Genre,
    GROUP_CONCAT (a.name, ', ') as "Leading Actors",
    CASE
        WHEN md.obtained = 1 THEN 'Yes'
        ELSE 'No'
    END AS Obtained
FROM
    media md
    left join movies mv on md.id = mv.media_id
    left join movie_genre_reference mgr on mv.id = mgr.movie_id
    left join genres g on mgr.genre_id = g.id
    left join actor_movie_reference amr on mv.id = amr.movie_id
    left join actors a on amr.actor_id = a.id
WHERE
    md.type = 'movie'
GROUP BY
    md.id
ORDER BY
    md.sort_title ASC;

-- name: get_movie_by_id
SELECT
    md.id as ID,
    md.title as Title,
    md.rating as Rating,
    mv.year as Year,
    g.name as Genre,
    GROUP_CONCAT (a.name, ', ') as "Leading Actors",
    CASE
        WHEN md.obtained = 1 THEN 'Yes'
        ELSE 'No'
    END AS Obtained
FROM
    media md
    left join movies mv on md.id = mv.media_id
    left join movie_genre_reference mgr on mv.id = mgr.movie_id
    left join genres g on mgr.genre_id = g.id
    left join actor_movie_reference amr on mv.id = amr.movie_id
    left join actors a on amr.actor_id = a.id
WHERE
    md.type = 'movie'
    AND md.id = '{{id}}'
GROUP BY
    md.id
ORDER BY
    md.sort_title ASC;

--name: get_movies_by_genre
SELECT
    md.title as Title,
    md.rating as Rating,
    mv.year as Year,
    g.name as Genre,
    GROUP_CONCAT (a.name, ', ') as "Leading Actors",
    CASE
        WHEN md.obtained = 1 THEN 'Yes'
        ELSE 'No'
    END AS Obtained
FROM
    media md
    left join movies mv on md.id = mv.media_id
    left join movie_genre_reference mgr on mv.id = mgr.movie_id
    left join genres g on mgr.genre_id = g.id
    left join actor_movie_reference amr on mv.id = amr.movie_id
    left join actors a on amr.actor_id = a.id
WHERE
    md.type = 'movie'
    AND g.name = '{{genre}}'
GROUP BY
    md.id
ORDER BY
    md.sort_title ASC;