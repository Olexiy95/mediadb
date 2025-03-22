import sqlite3


class MediaDB:
    """
    Handles CRUD operations for media records.
    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def get_movies(self):
        """Retrieve all movies with a new connection."""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT 
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
                        md.sort_title ASC;"""
            )
            return cursor.fetchall()

    def insert_movie(self, title, year, duration, rating):
        """Insert a new movie into the database."""
        pass

    def update_movie(self, movie_id, title=None, year=None, duration=None, rating=None):
        """Update movie details by ID."""
        pass

    def delete_movie(self, movie_id):
        """Delete a movie by ID."""
        pass

    def get_shows(self):
        """Retrieve all shows."""
        pass

    def insert_show(self, title, start_year, end_year, network, rating):
        """Insert a new show into the database."""
        pass

    def update_show(
        self,
        show_id,
        title=None,
        start_year=None,
        end_year=None,
        network=None,
        rating=None,
    ):
        """Update show details by ID."""
        pass

    def delete_show(self, show_id):
        """Delete a show by ID."""
        pass

    def get_media_by_type(self, media_type):
        """Retrieve media by type (movie, show, etc.)."""
        pass

    def get_actors(self):
        """Retrieve all actors."""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM actors;")
            return cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
