from pipeline import ranking_movies


def test_rank_movies_has_function():
    """Ensure the ranking_movies module defines rank_movies() or main()."""
    assert hasattr(ranking_movies, "rank_movies") or hasattr(ranking_movies, "main")


def test_precision_recall_at_k_returns_tuple():
    """Ensure precision_recall_at_k returns a 2-value tuple."""
    dummy_preds = [(1, 1, 4.0, 4.0, None)]
    result = ranking_movies.precision_recall_at_k(dummy_preds, k=1)
    assert isinstance(result, tuple)
    assert len(result) == 2
