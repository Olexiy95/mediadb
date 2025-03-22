from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from collections import defaultdict
from db_control import MediaDB

app = FastAPI()
mediaDB = MediaDB("test.db")
templates = Jinja2Templates(directory="templates")


@app.get("/actors/")
def list_actors(request: Request):
    """Returns a list of unique actors with the number of movies they appear in."""
    actors = mediaDB.get_actors()
    print("actors", actors)
    return templates.TemplateResponse(
        "actors.html", {"request": request, "actors": actors}
    )


@app.get("/")
def read_movies(request: Request):
    movies = mediaDB.get_movies()
    return templates.TemplateResponse(
        "index.html", {"request": request, "movies": movies}
    )


@app.get("/movie/{movie_id}")
def movie_detail(request: Request, movie_id: int):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()
    conn.close()

    if movie is None:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )

    return templates.TemplateResponse(
        "movie_detail.html", {"request": request, "movie": movie}
    )


@app.post("/update_movie/{movie_id}")
async def update_movie(movie_id: int, request: Request):
    """Updates a movie entry in the database."""
    conn = get_db_connection()
    data = await request.json()  # Get JSON data from request

    try:
        conn.execute(
            """
            UPDATE movies
            SET title = ?, year = ?, genre = ?, leading_actors = ?, rating = ?, notes = ?, obtained = ?
            WHERE id = ?
        """,
            (
                data["title"],
                data["year"],
                data["genre"],
                data["leading_actors"],
                data["rating"],
                data["notes"],
                data["obtained"],
                movie_id,
            ),
        )

        conn.commit()
        conn.close()
        return JSONResponse({"success": True})
    except Exception as e:
        conn.close()
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
