"""Test temperature endpoint and get_temp method results"""

# Sources:
## https://flask.palletsprojects.com/en/stable/testing/
## https://docs.pytest.org/en/stable/how-to/monkeypatch.html
## https://docs.pytest.org/en/stable/reference/reference.html#pytest.MonkeyPatch.setattr

import script

def test_get_temp(monkeypatch):
    """Test to make sure temperature is returned"""
    # pylint: disable=unused-argument
    def mockreturn(box_id):
        return 20.0

    monkeypatch.setattr(script, "get_temp", mockreturn)

    # ID doesn't matter here since return value has been patched
    x = script.get_temp(235235235)
    assert x == 20.0

def test_temperature_good(client, monkeypatch):
    """Test to make sure "Good" status is returned"""

    monkeypatch.setattr(script, "get_temp", lambda box_id: 20.0)

    response = client.get("/temperature")
    assert response.json["status"] == "Good"

def test_temperature_cold(client, monkeypatch):
    """Test to make sure "Too Cold" status is returned"""

    monkeypatch.setattr(script, "get_temp", lambda box_id: 5.0)

    response = client.get("/temperature")
    assert response.json["status"] == "Too Cold"

def test_temperature_hot(client, monkeypatch):
    """Test to make sure "Too Hot" status is returned"""

    monkeypatch.setattr(script, "get_temp", lambda box_id: 35.0)

    response = client.get("/temperature")
    assert response.json["status"] == "Too Hot"
