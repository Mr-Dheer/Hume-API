import requests

# Define the URL for the API endpoints
TOOLS_URL = "https://api.hume.ai/v0/evi/tools"
CONFIG_URL = "https://api.hume.ai/v0/evi/configs"

# Define your Hume API key
HUME_API_KEY = "nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj"

# Define the request headers with the API key
headers = {
    "X-Hume-Api-Key": HUME_API_KEY,
    "Content-Type": "application/json"
}

# Define the request body for creating the tool
TOOL_REQUEST_BODY = {
    "name": "get_current_weather-4",
    "version_description": "Fetches current weather and uses celsius or fahrenheit based on user's location.",
    "description": "This tool is for getting the current weather.",
    "parameters": "{\"type\": \"object\", \"properties\": { \"location\": { \"type\": \"string\", \"description\": \"The city and state, e.g. San Francisco, CA\" }, \"format\": { \"type\": \"string\", \"enum\": [\"celsius\", \"fahrenheit\"], \"description\": \"The temperature unit to use. Infer this from the users location.\" } }, \"required\": [\"location\", \"format\"] }"
}

# Make the POST request to create the tool
response = requests.post(TOOLS_URL, json=TOOL_REQUEST_BODY, headers=headers)

if response.status_code == 200:
    tool_info = response.json()
    tool_id = tool_info["id"]
    print("Tool created successfully!")
    print("Tool ID:", tool_id)
    print("Response:", tool_info)
else:
    print("Failed to create tool. Status code:", response.status_code)
    print("Response:", response.text)

    # Exit early if tool creation fails
    exit()

# Define the request body for creating the configuration
CONFIG_REQUEST_BODY = {
    "name": "Weather Assistant Config-4",
    "language_model": {
        "model_provider": "OPEN_AI",
        "model_resource": "gpt-3.5-turbo",
        "temperature": None
    },
    "tools": [
        {
            "id": tool_id,
            "version": 0
        }
    ]
}

# Make the POST request to create the configuration
response = requests.post(CONFIG_URL, json=CONFIG_REQUEST_BODY, headers=headers)

if response.status_code == 200:
    config_info = response.json()
    print('Configuration Created Successfully :D')
    print('Configuration ID:', config_info['id'])
    print('Response:', config_info)
else:
    print('Failed to create Configuration, Status Code:', response.status_code)
    print('Response:', response.text)
