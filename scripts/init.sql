-- Init scripts for creating core tables and relationships
CREATE TABLE
    media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        rating INTEGER,
        artwork_path TEXT,
        notes TEXT,
        obtained INTEGER,
        sort_title TEXT GENERATED ALWAYS AS (LOWER(title)),
        type TEXT NOT NULL CHECK (type IN ('movie', 'show', 'music')),
    );

CREATE TABLE
    movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        media_id INTEGER UNIQUE,
        year INTEGER,
        duration INTEGER,
        FOREIGN KEY (media_id) REFERENCES media (id)
    );

CREATE TABLE
    shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        media_id INTEGER UNIQUE,
        start_year INTEGER,
        end_year INTEGER,
        network TEXT,
        FOREIGN KEY (media_id) REFERENCES media (id)
    );

create table
    if not exists show_episodes (
        id INTEGER primary key AUTOINCREMENT,
        show_id integer,
        season_number integer,
        episode_number integer,
        episode_name text,
        FOREIGN key (show_id) REFERENCES shows (id)
    );

create table
    if not exists actors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        pseudonym TEXT
    );

create table
    if not exists actor_show_reference (
        show_id INTEGER,
        actor_id INTEGER,
        FOREIGN key (show_id) REFERENCES shows (id),
        foreign key (actor_id) REFERENCES actors (id)
    );

create table
    if not exists actor_movie_reference (
        movie_id INTEGER,
        actor_id INTEGER,
        FOREIGN key (movie_id) REFERENCES movies (id),
        foreign key (actor_id) REFERENCES actors (id)
    );

CREATE TABLE
    genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

CREATE TABLE
    movie_genre_reference (
        movie_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (movie_id) REFERENCES movies (id),
        FOREIGN KEY (genre_id) REFERENCES genres (id)
    );

CREATE TABLE
    show_genre_reference (
        show_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (show_id) REFERENCES shows (id),
        FOREIGN KEY (genre_id) REFERENCES genres (id)
    );