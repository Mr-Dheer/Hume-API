import requests
import uuid  # Import UUID module

# Define the URL for the API endpoint
TOOL_RESPONSE_URL = "https://api.hume.ai/v0/evi/tools"

# Define your Hume API key
HUME_API_KEY = "nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj"

# Define the request headers with the API key
headers = {
    "X-Hume-Api-Key": HUME_API_KEY,
    "Content-Type": "application/json"
}

# Function to simulate weather retrieval
def get_weather(location, format):
    # Simulate weather retrieval based on location and format
    return "60F"  # Hardcoded weather value

# Function to generate a UUID for the tool_call_id
def generate_tool_call_id():
    return str(uuid.uuid4())  # Generate a random UUID and convert it to string

# Function to handle tool calls
def handle_tool_call(name, parameters):
    try:
        # Generate a UUID for the tool_call_id
        tool_call_id = generate_tool_call_id()
        
        # Call the function to get weather information
        weather = get_weather(parameters["location"], parameters["format"])
        
        # Construct the tool_response message
        tool_response = {
            "type": "tool_response",
            "tool_call_id": tool_call_id,
            "content": weather
        }
        
        # Send the tool_response to EVI
        response = requests.post(f"{TOOL_RESPONSE_URL}/messages", json=tool_response, headers=headers)
        
        if response.status_code == 200:
            print("Tool response sent successfully!")
        else:
            print(f"Failed to send tool response. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Simulate receiving a tool_call message
tool_call_message = {
    "type": "tool_call",
    "tool_type": "function",
    "name": "get_current_weather",
    "parameters": {"location": "New York", "format": "fahrenheit"}
}

# Extract information from the tool_call message
name = tool_call_message["name"]
parameters = tool_call_message["parameters"]

# Handle the tool call
handle_tool_call(name, parameters)
