import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline import train

def test_train_imports():
    assert hasattr(train, "__name__")

def test_train_has_function():
    assert any(hasattr(train, f) for f in ["main", "train_model"])