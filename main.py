from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pickle.load(open("movies_df.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

class MovieRequest(BaseModel):
    movie: str

@app.get("/movies")
def get_movies():
    return {
        "movies": df["title"].tolist()
    }

@app.post("/recommend")
def recommend(request: MovieRequest):
    movie = request.movie.strip()

    if movie not in df['title'].values:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return {
        "recommended_movies": [
            df.iloc[i[0]].title for i in movies_list
        ]
    }
