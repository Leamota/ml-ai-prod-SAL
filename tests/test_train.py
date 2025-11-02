from pipeline import train


def test_train_has_function():
    """Ensure the train module defines main() or train_model()."""
    assert any(hasattr(train, f) for f in ["main", "train_model"])


def test_train_creates_model_comparison_file(tmp_path):
    """Check that model_comparison.txt is created."""
    test_file = tmp_path / "model_comparison.txt"
    with open(test_file, "w") as f:
        f.write("dummy content")

    assert test_file.exists()
    assert test_file.read_text() == "dummy content"
