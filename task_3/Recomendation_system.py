import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. LOAD DATASET
# ============================================================

# Get the folder where this Python file is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Create the complete path to movies.csv
csv_path = os.path.join(base_dir, "movies.csv")

# Check whether the CSV file exists
if not os.path.exists(csv_path):
    print("ERROR: movies.csv was not found!")
    print()
    print("Please make sure your folder contains:")
    print("  Recomendation_system.py")
    print("  movies.csv")
    print()
    print("Expected location:")
    print(csv_path)
    exit()


# Load the dataset
movies = pd.read_csv(csv_path)


# ============================================================
# 2. CHECK DATASET
# ============================================================

required_columns = ["title", "genre", "description"]

for column in required_columns:
    if column not in movies.columns:
        print(f"ERROR: Missing column '{column}' in movies.csv")
        print("Required columns:", required_columns)
        exit()


# Handle missing values
movies["genre"] = movies["genre"].fillna("")
movies["description"] = movies["description"].fillna("")


# ============================================================
# 3. CREATE FEATURES
# ============================================================

# Combine genre and description
movies["features"] = (
    movies["genre"] + " " + movies["description"]
)


# ============================================================
# 4. TF-IDF VECTORIZATION
# ============================================================

vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(
    movies["features"]
)


# ============================================================
# 5. CALCULATE COSINE SIMILARITY
# ============================================================

similarity_matrix = cosine_similarity(tfidf_matrix)


# ============================================================
# 6. RECOMMENDATION FUNCTION
# ============================================================

def recommend_movies(movie_title, number_of_recommendations=5):

    # Remove unnecessary spaces
    movie_title = movie_title.strip()

    # Find the movie
    movie_matches = movies[
        movies["title"].str.lower() == movie_title.lower()
    ]

    # If movie doesn't exist
    if movie_matches.empty:
        print()
        print("Movie not found!")
        print("Please select a movie from the available list.")
        return

    # Get movie index
    movie_index = movie_matches.index[0]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity_matrix[movie_index])
    )

    # Sort from highest similarity to lowest
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Display recommendations
    print()
    print("=" * 60)
    print(
        f"Recommendations based on: "
        f"{movies.iloc[movie_index]['title']}"
    )
    print("=" * 60)

    count = 0

    for index, score in similarity_scores:

        # Don't recommend the movie itself
        if index == movie_index:
            continue

        print(
            f"{count + 1}. "
            f"{movies.iloc[index]['title']}"
        )

        print(
            f"   Genre: {movies.iloc[index]['genre']}"
        )

        print(
            f"   Similarity Score: {score:.2f}"
        )

        print()

        count += 1

        if count >= number_of_recommendations:
            break


# ============================================================
# 7. DISPLAY AVAILABLE MOVIES
# ============================================================

print()
print("=" * 60)
print("          MOVIE RECOMMENDATION SYSTEM")
print("=" * 60)

print()
print("Available Movies:")
print("-" * 60)

for i, movie in enumerate(movies["title"], start=1):
    print(f"{i}. {movie}")


# ============================================================
# 8. USER INPUT
# ============================================================

print()

user_movie = input(
    "Enter the name of a movie you like: "
)


# Ask how many recommendations
try:
    number = int(
        input("How many recommendations do you want? ")
    )

    if number <= 0:
        print("Invalid number. Showing 5 recommendations.")
        number = 5

except ValueError:
    print("Invalid input. Showing 5 recommendations.")
    number = 5


# ============================================================
# 9. GENERATE RECOMMENDATIONS
# ============================================================

recommend_movies(
    user_movie,
    number
)


# ============================================================
# 10. END PROGRAM
# ============================================================

print()
print("=" * 60)
print("Thank you for using the Movie Recommendation System!")
print("=" * 60)