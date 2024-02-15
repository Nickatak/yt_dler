def test_sanity():
    assert True is True

    try:
        assert True is False
    except AssertionError as e:
        assert isinstance(e, AssertionError)
