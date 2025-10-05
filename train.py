import pandas as pd
from surprise import Dataset, Reader, KNNBasic, SVD
from surprise.model_selection import train_test_split, cross_validate, accuracy

# Load MovieLens data (replace with path to ml-latest-small/ratings.csv if local)
ratings = pd.read_csv("data/ratings.csv")

# Use Surprise Reader
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Train/test split
trainset, testset = train_test_split(data, test_size=0.2)

# --- Baseline Model (User-based KNN) ---
sim_options = {"name": "cosine", "user_based": True}
knn_model = KNNBasic(sim_options=sim_options)
knn_model.fit(trainset)

predictions = knn_model.test(testset)

print("KNN Model Performance:")
accuracy.rmse(predictions)
accuracy.mae(predictions)

# --- Stronger Model (SVD Matrix Factorization) ---
svd_model = SVD()
svd_model.fit(trainset)
predictions_svd = svd_model.test(testset)

print("\nSVD Model Performance:")
accuracy.rmse(predictions_svd)
accuracy.mae(predictions_svd)
