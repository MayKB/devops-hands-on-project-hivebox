"""Set up client for testing"""

import pytest
import script

@pytest.fixture()
def app():
    """Enable testing for application"""
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    """Set up client"""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Set up runner"""
    return app.test_cli_runner()
