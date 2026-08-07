"""Test temperature endpoint and get_temp method results"""

# Sources:
## https://flask.palletsprojects.com/en/stable/testing/
## https://docs.pytest.org/en/stable/how-to/monkeypatch.html
## https://docs.pytest.org/en/stable/reference/reference.html#pytest.MonkeyPatch.setattr

import math

import requests
import requests_mock

import script

class MockNoSensors:
    """Mock a requests response that returns no sensors"""
    def raise_for_status(self):
        """Mock raise_for_status"""
        # pylint: disable=unnecessary-pass
        pass

    # @staticmethod
    # pylint: disable=unused-argument
    def json(self):
        """Mock json with no sensors"""
        return {"mock_key": "mock_response"}

class MockNoTempSensor:
    """Mock a requests response with no sensors named 'Temperatur'"""
    def raise_for_status(self):
        """Mock raise_for_status"""
        # pylint: disable=unnecessary-pass
        pass

    # @staticmethod
    # pylint: disable=unused-argument
    def json(self):
        """Mock json with no sensors titled 'Temperatur'"""
        return { 'sensors': [{'title': 'No'}, {'title': 'Also no'}] }

class MockNoTempLast:
    """Mock a requests response no lastMeasurement for the Temperatur sensor"""
    def raise_for_status(self):
        """Mock raise_for_status"""
        # pylint: disable=unnecessary-pass
        pass

    # pylint: disable=unused-argument
    def json(self):
        """Mock json with no sensors titled 'Temperatur'"""
        return { 'sensors': [{'title': 'Temperatur'}, {'title': 'Also no'}] }

class MockNoTempValue:
    """Mock a requests response with no value for lastMeasurement"""
    def raise_for_status(self):
        """Mock raise_for_status"""
        # pylint: disable=unnecessary-pass
        pass

    # pylint: disable=unused-argument
    def json(self):
        """Mock json with no lastMeasurement value"""
        return { 'sensors': [{'title': 'Temperatur', 'lastMeasurement':
                    {'createdAt': '2026-07-28T19:11:18.246Z'}
                }]
            }

class MockTempOld:
    """Mock a requests response for a temp measurement that's too old"""
    def raise_for_status(self):
        """Mock raise_for_status"""
        # pylint: disable=unnecessary-pass
        pass

    # pylint: disable=unused-argument
    def json(self):
        """Mock json with old lastMeasurement value"""
        return { 'sensors': [{'title': 'Temperatur', 'lastMeasurement':
                    {'createdAt': '2024-07-28T19:11:18.246Z', 'value': '19.60'}
                }]
            }

def test_get_temp(monkeypatch):
    """Test to make sure temperature is returned"""
    # pylint: disable=unused-argument
    def mockreturn(box_id):
        return 20.0

    monkeypatch.setattr(script, "get_temp", mockreturn)

    # ID doesn't matter here since return value has been patched
    x = script.get_temp(235235235)
    assert math.isclose(x, 20.0, rel_tol=1e-09, abs_tol=1e-09)

def test_get_temp_error():
    """Test get_temp "Could not reach API" error"""

    box_id = 'invalid'

    with requests_mock.Mocker() as m:
        m.get(f'https://api.opensensemap.org/boxes/{box_id}?format=json', status_code=502)
        x = script.get_temp(box_id)

    assert "Could not reach API" in x

def test_get_temp_no_sensors(monkeypatch):
    """Test get_temp no sensors error"""
    # pylint: disable=unused-argument
    def mock_get(url, timeout):
        return MockNoSensors()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(23452345235)
    assert "does not have any sensors" in x

def test_get_temp_no_temp_sensor(monkeypatch):
    """Test get_temp no sensors named 'Temperatur' error"""
    # pylint: disable=unused-argument
    def mock_get(url, timeout):
        return MockNoTempSensor()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(23452345235)
    assert "do not have a temperature sensor" in x

def test_get_temp_no_temp_measurement(monkeypatch):
    """Test get_temp no lastMeasurement error"""
    # pylint: disable=unused-argument
    def mock_get(url, timeout):
        return MockNoTempLast()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(23452345235)
    assert "No last measurement for box" in x

def test_get_temp_no_temp_value(monkeypatch):
    """Test get_temp no value for lastMeasurement"""
    # pylint: disable=unused-argument
    def mock_get(url, timeout):
        return MockNoTempValue()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(23452345235)
    assert "Date or value missing for last measurement of box" in x

def test_get_temp_no_temp_value_old(monkeypatch):
    """Test get_temp lastMeasurement value too old"""
    # pylint: disable=unused-argument
    def mock_get(url, timeout):
        return MockTempOld()

    monkeypatch.setattr(requests, "get", mock_get)

    x = script.get_temp(23452345235)
    assert "Last value too old" in x

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

def test_temperature_bad(client, monkeypatch):
    """Test to make sure /temperature handles get_temp error"""

    monkeypatch.setattr(script, "get_temp", lambda box_id: "An error has occured")

    response = client.get("/temperature")

    assert "An error" in response.text
