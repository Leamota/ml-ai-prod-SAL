import pandas as pd
from stream.schema_validation import rating_schema


def test_schema_valid():
    df = pd.DataFrame({
        "userId": [1, 2],
        "movieId": [10, 20],
        "rating": [4.5, 3.0],
        "timestamp": [123456, 654321]
    })
    rating_schema.validate(df)
