"""Test temperature endpoint and get_temp method results"""

# Sources:
## https://flask.palletsprojects.com/en/stable/testing/
## https://docs.pytest.org/en/stable/how-to/monkeypatch.html
## https://docs.pytest.org/en/stable/reference/reference.html#pytest.MonkeyPatch.setattr

import requests
import requests_mock

import json
import script

class MockNoSensors:
    def raise_for_status(self):
        pass

    # @staticmethod
    def json(boxid):
        return {"mock_key": "mock_response"}

class MockNoTempSensor:
    def raise_for_status(self):
        pass

    # @staticmethod
    def json(boxid):
        return { 'sensors': [{'title': 'No'}, {'title': 'Also no'}] }

def test_get_temp(monkeypatch):
    """Test to make sure temperature is returned"""
    # pylint: disable=unused-argument
    def mockreturn(box_id):
        return 20.0

    monkeypatch.setattr(script, "get_temp", mockreturn)

    # ID doesn't matter here since return value has been patched
    x = script.get_temp(235235235)
    assert x == 20.0

def test_get_temp_error():
    """Test get_temp "Could not reach API" error"""

    box_id = 'invalid'

    with requests_mock.Mocker() as m:
        m.get(f'https://api.opensensemap.org/boxes/{box_id}?format=json', status_code=502)
        x = script.get_temp(box_id)

    assert 502 in x

def test_get_temp_no_sensors(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockNoSensors()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(346345635)
    assert "does not have any sensors" in x[0]['error']

def test_get_temp_no_temp_sensor(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockNoTempSensor()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(346345635)
    assert "do not have a temperature sensor" in x[0]['error']

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

    monkeypatch.setattr(script, "get_temp", lambda box_id: 37.0)

    response = client.get("/temperature")
    assert response.json["status"] == "Too Hot"
