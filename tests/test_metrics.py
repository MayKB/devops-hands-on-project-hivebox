"""Test temperature endpoint and get_temp method results"""
import script

def test_metrics_status(client):
    """Test to make sure metrics is a valid path"""
    response = client.get("/metrics")
    assert response.status_code == 200

def test_metrics_version(client):
    """Test to make sure metrics.info is working"""
    response = client.get("/metrics")
    assert b"app_info" in response.data
    