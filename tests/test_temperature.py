"""Test temperature endpoint and get_temp method results"""

# Sources:
## https://flask.palletsprojects.com/en/stable/testing/
## https://docs.pytest.org/en/stable/how-to/monkeypatch.html
## https://docs.pytest.org/en/stable/reference/reference.html#pytest.MonkeyPatch.setattr

import script

def test_get_temp(monkeypatch):
    """Test to make sure temperature is returned"""
    def mockreturn(id):
        return 20.0

    monkeypatch.setattr(script, "get_temp", mockreturn(id))

    # ID doesn't matter here since return value has been patched
    x = script.get_temp(235235235)
    assert x == 20.0

def test_temperature(client, monkeypatch):
    """Test to make sure status is returned"""

    monkeypatch.setattr(script, "get_temp", lambda box_id: 20.0)

    response = client.get("/temperature")
    assert response.json["status"] == "Good"
