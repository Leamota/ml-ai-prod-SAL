# train.py
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split, accuracy

# Load MovieLens data
ratings = pd.read_csv("data/ratings.csv")  # make sure this file exists

# Model 1: Popularity-based (most watched movies)
popularity = ratings.groupby('movieId')['rating'].count().sort_values(ascending=False)
top_movies = popularity.head(10)
print("Top 10 popular movies by count:\n", top_movies)

# Model 2: SVD (Collaborative Filtering)
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

svd = SVD()
svd.fit(trainset)
predictions = svd.test(testset)

# Evaluate
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

print(f"\nSVD Model Results: RMSE={rmse:.3f}, MAE={mae:.3f}")

# Save summary
with open("docs/model_comparison.txt", "w") as f:
    f.write("Model Comparison:\n")
    f.write("1. Popularity-Based (simple ranking)\n")
    f.write(f"2. SVD: RMSE={rmse:.3f}, MAE={mae:.3f}\n")

print("\nModel comparison saved to docs/model_comparison.txt")
