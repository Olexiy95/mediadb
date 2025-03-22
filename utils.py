import sqlite3
import csv

# DB Variables
DB_FILE = "media.db"
TABLE_NAME = "movies"
CSV_FILE = "csv/movies.csv"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


def fix_titles():
    cursor.execute(
        f"""BEGIN TRANSACTION;

            UPDATE movies
            SET title = 'The ' || substr(title, 1, length(title) - 5)
            WHERE title LIKE '%, The';

            UPDATE movies
            SET sort_title = CASE
            WHEN title LIKE 'The %' THEN substr(title, 5)
            ELSE title
            END;

            COMMIT;
            """
    )
    conn.commit()


def filter_movies_by_actor(actor_id):
    cursor.execute(
        "SELECT * FROM movies WHERE id IN (SELECT movie_id FROM actor_movie_reference WHERE actor_id = ?)",
        (actor_id,),
    )
    return cursor.fetchall()


def filter_actor_by_movie(movie_id):
    cursor.execute(
        "SELECT * FROM actors WHERE id IN (SELECT actor_id FROM actor_movie_reference WHERE movie_id = ?)",
        (movie_id,),
    )
    return cursor.fetchall()


# Function to clean and format rows
def clean_row(row):
    print("row: ", row)
    """Ensure row is valid and not entirely empty."""
    return any(row)


# Read and import CSV data
with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(
        csvfile, delimiter=","
    )  # Use tab as delimiter if CSV is tab-separated
    for row in reader:
        if not clean_row(row.values()):
            print("Skipping empty row...")
            continue  # Skip empty rows

        # Extract fields with fallback defaults (to avoid None issues)
        title = row.get("Title", "").strip()
        year = row.get("Year", "").strip() or None
        genre = row.get("Genre", "").strip()
        leading_actors = row.get("Leading Actor(s)", "").strip()
        rating = row.get("Rating", "").strip()
        notes = row.get("Notes", "").strip()
        obtained = (
            1 if row.get("Obtained", "").strip().lower() in ("yes", "true", "1") else 0
        )

        print("title: ", row.get("Title", ""))

        # Ensure at least title is present before inserting
        if not title:
            continue

        # Insert movie into database (ignore duplicates)
        cursor.execute(
            f"""
            INSERT INTO {TABLE_NAME} (title, year, genre, leading_actors, rating, notes, obtained)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
            (title, year, genre, leading_actors, rating, notes, obtained),
        )

# Commit changes and close connection
conn.commit()
conn.close()

print("Movie data imported successfully!")
