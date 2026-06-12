"""Test version endpoint result"""
from script import version

def test_version():
    """Test to make sure version is returned"""
    result = version()
    assert "version" in result
