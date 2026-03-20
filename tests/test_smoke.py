def test_import_app():
    from src import main

    assert hasattr(main, 'app')
