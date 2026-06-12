"""This app will show the most recent version and some sensebox data or something"""

# Sources:
## https://stackoverflow.com/questions/76082808/how-to-get-github-repo-latest-release-in-python

import requests
from datetime import datetime, timedelta, timezone
from flask import Flask
from github import Github

app = Flask(__name__)

@app.route("/temperature")
def temperature():
    """Get sensebox data and return average temperature from the last hour"""
    
    # Ids for senseboxes, given by tutorial
    ids = ['5eba5fbad46fb8001b799786', '5c21ff8f919bf8001adf2488', '5ade1acf223bd80019a1011c']
    # Total temperature from the senseboxes, start at 0 degrees
    total = 0
    # Get the current time
    cur_time = datetime.now(timezone.utc)
    
    # For each of the given boxes:
    for box_id in ids:
        # Get json results from API
        content = requests.get(f'https://api.opensensemap.org/boxes/{box_id}?format=json')
        # Check for successful connection
        if (content.status_code == 200):
            # Get all sensors from sensebox
            sensors = content.json()['sensors']
            # Loop through each of the sensors
            for sensor in sensors: 
                if sensor['title'] == 'Temperatur':
                    # If there is not a last measurement, or a date or value for that measurement, return and alert user
                    if sensor['lastMeasurement'] is None or sensor['lastMeasurement']['createdAt'] is None or sensor['lastMeasurement']['value'] is None:
                        return "No last measurement"
                    # See if last measurement was within the last hour
                    time_diff = cur_time - datetime.fromisoformat(sensor['lastMeasurement']['createdAt'])
                    recent = time_diff.total_seconds() < 3600
                    # If there is a temperature sensor, add its value to the sum
                    if recent:
                        total += float(sensor['lastMeasurement']['value'])
        else: # If connection failed, return and alert user
            return "Could not connect to API"
    
    # Divide the sum of all the temperatures by 3 to get the average
    avg = total/3
    
    # Return the sum and average
    return {"totaltemp": total, "averagetemp": avg}

@app.route('/version')
def version():
    """Get most recent app version"""
    token = None
    repo_path = "MayKB/devops-hands-on-project-hivebox"
    g = Github(token)
    repo = g.get_repo(repo_path)
    latest = repo.get_latest_release()
    return {"version": latest.name}
