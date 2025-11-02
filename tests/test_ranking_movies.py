import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline import ranking_movies


def test_rank_movies_imports():
    assert hasattr(ranking_movies, "__name__")


def test_rank_movies_has_function():
    assert hasattr(ranking_movies, "rank_movies") or hasattr(ranking_movies, "main")
