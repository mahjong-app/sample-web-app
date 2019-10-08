import pytest
import os
from mahjong_sample_web_app.run import create_app


@pytest.fixture
def base():
    return {}


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    config = os.environ.get("CONFIG", "local_test")
    app = create_app(config)
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()
