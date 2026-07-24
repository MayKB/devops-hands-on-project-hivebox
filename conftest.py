"""Set up client for testing"""

import pytest
from script import app

# pylint: disable=redefined-outer-name
# pylint: disable=function-redefined
@pytest.fixture()
def app():
    """Enable testing for application"""
    app.config.update({
        "TESTING": True,
    })

    yield app

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
