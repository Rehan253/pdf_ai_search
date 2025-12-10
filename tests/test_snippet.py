from search_engine import generate_snippet


def test_snippet_basic():
    text = "The weather was bad. Engine failed during takeoff. Visibility was low."
    query = "weather"

    snippet = generate_snippet(text, query)

    # Should contain matching word
    assert "weather" in snippet.lower()

    # Snippet must not be empty
    assert len(snippet) > 0


def test_snippet_no_match_fallback():
    text = "This sentence has no relation to the query."
    query = "rainstorm"

    snippet = generate_snippet(text, query)

    # Fallback should still return a string
    assert isinstance(snippet, str)
    assert len(snippet) > 0
