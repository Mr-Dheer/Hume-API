import requests

# Define the URL for the API endpoint
CONFIG_URL = 'https://api.hume.ai/v0/evi/configs'

# Define your Hume API key
HUME_API_KEY = 'nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj'

# Define the request headers with the API key
headers = {
    'X-Hume-Api-Key': HUME_API_KEY,
    'Content-Type': 'application/json'
}

# Define the request body for creating the configuration
CONFIG_REQUEST_BODY = {
    "name": "Weather Assistant Config",
    "language_model": {
        "model_provider": "OPEN_AI",
        "model_resource": "gpt-3.5-turbo",
        "temperature": None
    },
    "tools": [
        {
            "id": "15c38b04-ec9c-4ae2-b6bc-5603512b5d00",
            "version": 0
        }
    ]
}

# Make the POST request to create the configuration
response = requests.post(CONFIG_URL, json=CONFIG_REQUEST_BODY, headers=headers)

if response.status_code == 200:
    config_info = response.json()
    config_id = config_info['id']  # Extract the configuration ID from the response
    print('Configuration Created Successfully :D')
    print('Configuration ID:', config_id)
    print('Response:', config_info)
    
    # Store the configuration ID for future use
    with open('config_id.txt', 'w') as file:
        file.write(config_id)
else:
    print('Failed to create Configuration, Status Code:', response.status_code)
    print('Response:', response.text)
