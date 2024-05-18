import requests
import asyncio
import websockets
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
    "name": "get_current_weather-16",
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
    print('Paaji Tuada Naam Kya hai:', tool_info['name'])
    print("Response:", tool_info)

else:
    print("Failed to create tool. Status code:", response.status_code)
    print("Response:", response.text)

    # Exit early if tool creation fails
    exit()

# Define the request body for creating the configuration
CONFIG_REQUEST_BODY = {
    "name": "Weather Assistant Config-16",
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
    config_id = config_info['id']
    print('Configuration Created Successfully :D')
    print('Tuada Naam ke hai Paaji:', config_info['name'])
    print('Configuration ID:', config_info['id'])
    print('Response:', config_info)
else:
    print('Failed to create Configuration, Status Code:', response.status_code)
    print('Response:', response.text)



#! Need to fix this below
# #  Define the request body for invoking the configuration
# INVOKE_REQUEST_BODY = {
#     "config_id": config_id,
#     "input": {
#         "text": "What's the weather like in San Francisco, CA?",
#         "context": {}
#     }
# }

# # Make the POST request to invoke the configuration
# response = requests.post("https://api.hume.ai/v0/evi/chat?", json=INVOKE_REQUEST_BODY, headers=headers)



# if response.status_code == 200:
#     invoke_response = response.json()
#     response_text = invoke_response['response']['text']
#     print(f"Response from Hume: {response_text}")
# else:
#     print(f"Failed to invoke configuration. Status code: {response.status_code}")
#     print(f"Response: {response.text}")

