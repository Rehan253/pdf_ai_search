from search_engine import SearchEngine


def test_search_returns_valid_structure():
    engine = SearchEngine()
    
    results = engine.search("weather", k=3, threshold=2.0)

    # Always returns a list
    assert isinstance(results, list)

    if results:
        first = results[0]
        
        assert "distance" in first
        assert "metadata" in first
        
        meta = first["metadata"]

        assert "filename" in meta
        assert "page" in meta
