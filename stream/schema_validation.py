from pandera import Column, DataFrameSchema, Check
import pandas as pd

# Define what each column should look like
rating_schema = DataFrameSchema(
    {
        "userId": Column(int, Check.ge(0)),
        "movieId": Column(int, Check.ge(0)),
        "rating": Column(float, Check.between(0.5, 5.0)),
        "timestamp": Column(int, Check.ge(0)),
    }
)

# Example usage
if __name__ == "__main__":
    df = pd.read_csv("data/ratings.csv")
    validated_df = rating_schema.validate(df)
    print("✅ Schema validated successfully!")
