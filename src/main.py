from fastapi import FastAPI

app = FastAPI()


movies = [
    {
        "id": 1,
        "title": "The Matrix",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "year": 1999,
        "rating": 8.7,
        "category": "Science Fiction"
    },
    {
        "id": 2,
        "title": "The Matrix",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "year": 1999,
        "rating": 8.7,
        "category": "Science Fiction"
    },
    {
        "id": 3,
        "title": "The Matrix",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "year": 1999,
        "rating": 8.7,
        "category": "Science Fiction"
    }
]

@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/movies/{id}")
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return {"message": "Pelicula no encontrada"}


