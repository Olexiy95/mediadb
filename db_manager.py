import sqlite3
import pandas as pd


class MediaDBManager:
    def __init__(self, db_path, movies_csv, shows_csv, sql_file="scripts/init.sql"):
        self.db_path = db_path
        self.movies_csv = movies_csv
        self.shows_csv = shows_csv
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.sql_file = sql_file

    def initialise_database(self):
        """Reads and executes SQL statements from a file to set up the database schema."""
        try:
            with open(self.sql_file, "r") as f:
                sql_script = f.read()

            self.cursor.executescript(sql_script)
            self.conn.commit()
            print(f"Database schema initialized from {self.sql_file}")
        except sqlite3.Error as e:
            print(f"Error executing SQL script: {e}")

    def process_titles(self, title):
        """Reformat titles from old CSV to match new format."""
        if ", The" in title:
            return "The " + title.replace(", The", "")
        return title

    def insert_genres(self, genres=None, csv_file=None):
        """Insert genres into the database if they don't exist."""
        genre_list = set()  # Use a set to prevent duplicates before inserting

        if csv_file:
            df = pd.read_csv(csv_file)
            # Split multiple genres per row, flatten the list
            genre_list.update(
                g.strip()
                for genre_string in df["Genre"].dropna()
                for g in genre_string.split(",")
            )
        elif genres:
            # Process single input genre string
            genre_list.update(g.strip() for g in genres.split(","))

        # Insert genres, ignoring duplicates
        for genre in genre_list:
            self.cursor.execute(
                "INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre,)
            )

        self.conn.commit()

    def insert_actors(self, actors=None, csv_file=None):
        """Insert actors into the database if they don't exist."""
        actor_list = set()  # Use a set to prevent duplicate insertions

        if csv_file:
            df = pd.read_csv(csv_file)
            # Extract actors, handle missing values, and split multiple names per row
            actor_list.update(
                a.strip()
                for actor_string in df["Leading Actor(s)"].dropna()
                for a in actor_string.split(",")
            )
        elif actors:
            # Process single input actor string
            actor_list.update(a.strip() for a in actors.split(","))

        # Insert actors, ignoring duplicates
        for actor in actor_list:
            self.cursor.execute(
                "INSERT OR IGNORE INTO actors (name) VALUES (?)", (actor,)
            )

        self.conn.commit()

    def insert_movies(self):
        """Insert movies and link genres/actors properly using Pandas."""
        df = pd.read_csv(self.movies_csv)

        print("dataframe obrtained")

        # Normalize title (fix "Inbetweeners, The" -> "The Inbetweeners")
        df["Title"] = df["Title"].apply(self.process_titles)

        # Convert columns to appropriate types
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna("0").astype(int)
        df["Obtained"] = df["Obtained"].fillna("0").astype(int)
        df["Rating"] = df["Rating"].fillna("0")
        df["Notes"] = df["Notes"].fillna("")
        df["Leading Actor(s)"] = df["Leading Actor(s)"].dropna()
        df["Genre"] = df["Genre"].dropna()

        # Iterate over rows and insert into the database
        for _, row in df.iterrows():
            self.cursor.execute(
                "INSERT INTO media (title, rating, notes, obtained) VALUES (?, ?, ?, ?)",
                (row["Title"], row["Rating"], row["Notes"], row["Obtained"]),
            )
            media_id = self.cursor.lastrowid

            self.cursor.execute(
                "INSERT INTO movies (media_id, year) VALUES (?, ?)",
                (media_id, row["Year"]),
            )
            movie_id = self.cursor.lastrowid

            leading_actors = row["Leading Actor(s)"]
            print("leading_actors", leading_actors)
            if pd.notna(leading_actors) and leading_actors is not None:
                for actor in leading_actors.split(","):
                    print("actor", actor)
                    actor_id = self.cursor.execute(
                        "SELECT id FROM actors WHERE name = ?", (actor.strip(),)
                    ).fetchone()[0]
                    print("actor_id", actor_id)
                    self.cursor.execute(
                        "INSERT INTO actor_movie_reference (actor_id, movie_id) VALUES (?, ?)",
                        (actor_id, movie_id),
                    )

            genres = row["Genre"]
            print("genres", genres)

            # Skip if the value is empty or NaN
            if pd.notna(genres) and genres is not None:
                print("genres", genres, type(genres))

                for g in genres.split(","):  # No need for nested loops
                    g = g.strip()
                    if not g:  # Skip empty genre names
                        continue

                    print("genre", g)

                    genre_id = self.cursor.execute(
                        "SELECT id FROM genres WHERE name = ?", (g,)
                    ).fetchone()

                    if genre_id:  # Ensure genre exists before inserting
                        self.cursor.execute(
                            "INSERT INTO movie_genre_reference (genre_id, movie_id) VALUES (?, ?)",
                            (genre_id[0], movie_id),
                        )
        self.conn.commit()
        print("Movies inserted successfully.")

    def full_run(self):
        """Runs the full init process in order."""
        print("Inserting genres...")
        print("Inserting actors...")
        print("Inserting movies...")
        self.insert_movies()
        print("Data import complete.")

    def close(self):
        """Close the database connection."""
        self.conn.close()
