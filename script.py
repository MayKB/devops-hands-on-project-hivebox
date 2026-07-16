"""This app can show the most recent version of the project on github, 
return metrics about the app and retrieve temperature data from three SenseBoxes"""

# Sources:
## https://stackoverflow.com/questions/76082808/how-to-get-github-repo-latest-release-in-python
## https://www.codecademy.com/article/python-environment-variables

import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from github import Github
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

@app.route("/temperature", methods=['GET'])
def temperature():
    """Get sensebox data and return average temperature from the last hour"""

    # Ids for senseboxes, given by tutorial
    ids = [os.getenv("SENSEBOX_ID_1"), os.getenv("SENSEBOX_ID_2"), os.getenv("SENSEBOX_ID_3")]
    # Total temperature from the senseboxes, start at 0 degrees
    total = 0

    # For each of the given boxes:
    for box_id in ids:

        try:
            url = f'https://api.opensensemap.org/boxes/{box_id}?format=json'
            sense = requests.get(url, timeout=10)
            sense.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Could not reach API for box {box_id}: {e}"}, 502

        # Get all sensors from sensebox
        sensors = sense.json()['sensors']

        # Loop through each of the sensors to find the temperature sensor
        for sensor in sensors:
            if sensor['title'] == 'Temperatur':
                temp_sensor = sensor

        # If no temperature sensor was found, return and alert
        if temp_sensor is None:
            return {"error": "One or more boxes do not have a temperature sensor"}, 200

        # If no last measurement was found, return and alert
        if temp_sensor['lastMeasurement'] is None:
            return {"error": f"No last measurement for box {box_id}"}, 200

        s_created_at = temp_sensor['lastMeasurement']['createdAt']
        s_value = temp_sensor['lastMeasurement']['value']

        # If date or value for last measurement, return and alert
        if s_created_at is None or s_value is None:
            return {"error": f"Date or value missing for last measurement of box {box_id}"}, 200

        # See if last measurement was within the last hour
        measure_time = datetime.fromisoformat(s_created_at)
        recent = (datetime.now(timezone.utc) - measure_time) < 3600

        # If there is a recent temperature value, add its value to the sum
        if recent:
            total += float(s_value)
        else:
            return {"error": f"Last value too old for {box_id}, {s_created_at}"}, 200

    # Divide the sum of all the temperatures by 3 to get the average
    avg = total/3

    # Determine status message
    if avg < 11:
        status = "Too Cold"
    elif avg > 36:
        status = "Too Hot"
    else:
        status = "Good"

    # Return the sum and average
    return {"boxid1": ids[0], "boxid2": ids[1], "boxid3": ids[2],
            "totaltemp": total, "averagetemp": avg, "status": status}

@app.route('/version', methods=['GET'])
def version():
    """Get most recent app version"""
    token = None
    repo_path = "MayKB/devops-hands-on-project-hivebox"
    g = Github(token)
    repo = g.get_repo(repo_path)
    latest = repo.get_latest_release()
    return {"version": latest.name}

# Get default Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version=version()['version'])
