"""Set up client for testing"""

import pytest
from script import app as flask_app

@pytest.fixture()
def app():
    """Enable testing for application"""
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app

# pylint: disable=redefined-outer-name
@pytest.fixture()
def client(app):
    """Set up client"""
    return app.test_client()

# pylint: disable=redefined-outer-name
@pytest.fixture()
def runner(app):
    """Set up runner"""
    return app.test_cli_runner()
