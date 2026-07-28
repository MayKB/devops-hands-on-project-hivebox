import json

@staticmethod
def json():
    mock_sensors: {
        "sensors": [
            {
                "title": "No"
            },
            {
                "title": "Also No"
            }
        ]
    }
    return json.dumps(mock_sensors)
    
print(json())