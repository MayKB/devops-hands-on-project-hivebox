from script import version

def test_version():
    result = version()
    assert "version" in result