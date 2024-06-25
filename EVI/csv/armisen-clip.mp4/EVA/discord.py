import requests
import json

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
    "name": "get-current-weather-11",
    "description": "Fetches current weather and uses Celsius or Fahrenheit based on user's location.",
    "tool_config": {
        "model_inputs": [
            {
                "name": "location",
                "description": "The city and state, e.g., San Francisco, CA",
                "type": "string",
                "format": {"type": "string"},
                "required": True
            },
            {
                "name": "temperature_unit",
                "description": "The temperature unit to use. Infer this from the user's location.",
                "type": "string",
                "format": {"type": "string"},
                "required": False
            }
        ]
    }
}

# Make the POST request to create the tool
response = requests.post(TOOLS_URL, json=TOOL_REQUEST_BODY, headers=headers)

if response.status_code == 200:
    tool_info = response.json()
    tool_id = tool_info['id']
    tool_name = tool_info['name']
    print(f"Tool '{tool_name}' created successfully with ID: {tool_id}")
else:
    print(f"Failed to create tool. Status code: {response.status_code}")
    print(f"Response: {response.text}")
    exit()

# Define the request body for creating the configuration
CONFIG_REQUEST_BODY = {
    "name": "Weather Assistant Config-11",
    "language_model": {
        "model_provider": "OPEN_AI",
        "model_resource": "gpt-3.5-turbo"
    },
    "tools": [
        {
            "id": tool_id,
            "version": "0"
        }
    ]
}

# Make the POST request to create the configuration
response = requests.post(CONFIG_URL, json=CONFIG_REQUEST_BODY, headers=headers)

if response.status_code == 200:
    config_info = response.json()
    config_id = config_info['id']
    config_name = config_info['name']
    print(f"Configuration '{config_name}' created successfully with ID: {config_id}")
else:
    print(f"Failed to create configuration. Status code: {response.status_code}")
    print(f"Response: {response.text}")
    exit()

# Define the request body for invoking the configuration
INVOKE_REQUEST_BODY = {
    "config_id": config_id,
    "input": {
        "text": "What's the weather like in San Francisco, CA?",
        "context": {}
    }
}

# Make the POST request to invoke the configuration
response = requests.post("wss://api.hume.ai/v0/evi/chat?", json=INVOKE_REQUEST_BODY, headers=headers)

if response.status_code == 200:
    invoke_response = response.json()
    response_text = invoke_response['response']['text']
    print(f"Response from Hume: {response_text}")
else:
    print(f"Failed to invoke configuration. Status code: {response.status_code}")
    print(f"Response: {response.text}")
