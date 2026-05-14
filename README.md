# Movie Recommender System

A content-based movie recommendation web app built with Python and Streamlit.

Live app: https://kumar-movie-recommender.streamlit.app/

Created by: Kumar Gaurav

## Project Overview

This project recommends movies similar to the one selected by the user. It uses movie metadata such as overview, genres, keywords, cast, and crew to understand the content of each movie. The app converts this textual information into numerical vectors and compares movies using similarity scores.

The final application is deployed with Streamlit and displays recommended movie titles along with posters fetched from the TMDB API.

## Problem Statement

When a user likes a movie, they often want to discover similar movies. The goal of this project is to build a simple recommendation system that can answer:

```text
If the user selects one movie, which other movies are most similar to it?
```

Instead of using user ratings or watch history, this project uses the movie's own content. This approach is called content-based filtering.

## Dataset

The project uses TMDB movie data. During development, the raw data came from:

```text
tmdb_5000_movies.csv
tmdb_5000_credits.csv
```

These CSV files contain information such as:

```text
movie_id
title
overview
genres
keywords
cast
crew
```

The raw CSV files are not pushed to GitHub because they are large and only needed during preprocessing.

## How The Recommendation System Works

### 1. Data Loading

The movie and credits CSV files are loaded using pandas:

```python
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")
```

Both datasets are merged so that each movie has its metadata and credit information in one dataframe.

### 2. Feature Selection

Only the useful columns are kept:

```text
movie_id
title
overview
genres
keywords
cast
crew
```

These columns help describe what a movie is about.

### 3. Data Cleaning

Missing values are removed. JSON-like text columns such as genres, keywords, cast, and crew are converted into Python lists.

For example, genres are converted from raw structured text into:

```python
["Action", "Science Fiction", "Adventure"]
```

For cast, only the top actors are used. For crew, the director is extracted.

### 4. Creating Tags

The important text features are combined into one column called `tags`.

Example:

```text
overview + genres + keywords + cast + director
```

This creates a single text representation of each movie.

For example, a movie's tags may contain words like:

```text
space future alien adventure samworthington jamescameron
```

This combined text becomes the base for comparing movies.

### 5. Text Vectorization

Computers cannot directly compare text, so the text must be converted into numbers.

Each movie is represented as a vector. A vector is a list of numbers that represents the words present in a movie's tags.

Simple example:

```text
Vocabulary: ["space", "alien", "love", "war"]

Movie A: "space alien space"
Vector A: [2, 1, 0, 0]

Movie B: "space war"
Vector B: [1, 0, 0, 1]
```

Here, each number shows how many times a word appears in the movie's tags.

### 6. Similarity Matching

After converting movies into vectors, the system compares one movie vector with every other movie vector.

This project uses cosine similarity.

Cosine similarity checks the angle between two vectors. If two movies have similar words in their tags, their vectors point in a similar direction, and their similarity score is higher.

High similarity means:

```text
The movies are close in meaning/content.
```

Low similarity means:

```text
The movies are different in meaning/content.
```

### 7. Recommendation Logic

When the user selects a movie:

1. The app finds that movie's index.
2. It gets the similarity scores for that movie.
3. It sorts all other movies by similarity score.
4. It selects the top 5 most similar movies.
5. It displays their names and posters.

Core logic:

```python
movie_index = movies[movies["title"] == movie].index[0]
distances = similarity[movie_index]
movie_list = sorted(
    list(enumerate(distances)),
    reverse=True,
    key=lambda x: x[1],
)[1:6]
```

The `[1:6]` is used because the first result is the selected movie itself, so it is skipped.

## Application Flow

The deployed Streamlit app follows this flow:

```text
Load movies_dict.pkl and similarity_dict.pkl
Display movie dropdown
User selects a movie
User clicks Recommend
Find top 5 similar movies
Fetch posters from TMDB API
Display recommendations in columns
```

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── movies_dict.pkl
├── similarity_dict.pkl
└── .gitignore
```

### app.py

The main Streamlit app. It loads the saved data, handles recommendation logic, fetches posters, and displays the UI.

### movies_dict.pkl

A preprocessed movie dataset saved as a pickle file. This avoids preprocessing the raw CSV files every time the app starts.

### similarity_dict.pkl

The precomputed similarity matrix. This stores how similar every movie is to every other movie.

### requirements.txt

Contains the Python packages required to run the app.

### .gitignore

Keeps unnecessary files out of GitHub, including raw CSVs, cache files, virtual environments, and local secrets.

## Why Pickle Files Are Used

Preprocessing text and calculating similarity can take time. To make the app faster, the processed movie data and similarity matrix are saved as `.pkl` files.

At runtime, the app directly loads:

```python
movies_dict.pkl
similarity_dict.pkl
```

This makes the deployed app faster and simpler.

## TMDB Poster API

Movie posters are fetched using the TMDB API.

The app expects an API key from either:

```text
Streamlit secrets
```

or:

```text
TMDB_API_KEY environment variable
```

In Streamlit Cloud, the secret should be added like this:

```toml
tmdb_api_key = "your_tmdb_api_key_here"
```

The app does not store the API key directly in the code.

## Installation

Clone the repository:

```bash
git clone https://github.com/gaurav7979077511/Movie-recomender-system.git
cd Movie-recomender-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the TMDB API key:

```bash
export TMDB_API_KEY="your_api_key_here"
```

Run the app:

```bash
streamlit run app.py
```

## Deployment

The app is deployed on Streamlit Community Cloud.

Deployment settings:

```text
Repository: gaurav7979077511/Movie-recomender-system
Branch: main
Main file path: app.py
App URL: https://kumar-movie-recommender.streamlit.app/
```

## What I Learned

While building this project, I learned:

- How content-based recommendation systems work.
- How movie metadata can be combined into a single text feature.
- How text can be converted into numerical vectors.
- How vectors allow movies to be compared mathematically.
- How cosine similarity is used to find movies with similar content.
- How preprocessing improves the quality of recommendations.
- How pickle files can be used to save processed data and speed up app loading.
- How to build an interactive web app with Streamlit.
- How to manage project files using `.gitignore`.
- How to push only required files to GitHub.
- How to deploy a Python app on Streamlit Community Cloud.

## Limitations

- The app uses content-based filtering only.
- It does not use user ratings or user behavior.
- Recommendations depend on the quality of the movie metadata.
- The similarity matrix file is large because it stores movie-to-movie similarity scores.
- Posters require a valid TMDB API key.

## Future Improvements

Possible improvements:

- Add search support for movie names.
- Show similarity scores with recommendations.
- Add movie overview, release date, and rating.
- Improve UI styling.
- Use Git LFS or external storage for large model files.
- Add collaborative filtering using user ratings.
- Add hybrid recommendations by combining content similarity and popularity.

## Tech Stack

```text
Python
pandas
NumPy
Streamlit
requests
TMDB API
GitHub
Streamlit Community Cloud
```

## Author

Kumar Gaurav
