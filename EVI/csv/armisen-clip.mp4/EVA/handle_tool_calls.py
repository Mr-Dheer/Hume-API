import requests

# Define the URL for the API endpoints
TOOL_CALL_URL = "https://api.hume.ai/v0/evi/tools/c7eba503-42e2-48ab-b106-08176035402e"
RESPONSE_URL = "https://api.hume.ai/v0/evi/response"

# Define your Hume API key
HUME_API_KEY = "nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj"

# Define the request headers with the API key
headers = {
    "X-Hume-Api-Key": HUME_API_KEY,
    "Content-Type": "application/json"
}

# Listen for tool_call messages
def listen_for_tool_call():
    while True:
        # Make a GET request to retrieve tool_call messages
        response = requests.get(TOOL_CALL_URL, headers=headers)
        
        if response.status_code == 200:
            tool_call = response.json()
            print("Received tool_call message:", tool_call)  # Add this line for debugging
            # Check if it's a tool_call message
            if "type" in tool_call and tool_call["type"] == "tool_call":
                process_tool_call(tool_call)
            else:
                print("Received message is not a tool_call message.")
        else:
            print("Failed to fetch tool_call message. Status code:", response.status_code)


# Process tool_call message
def process_tool_call(tool_call):
    # Extract necessary information
    tool_call_id = tool_call["tool_call_id"]
    parameters = tool_call["parameters"]
    
    # Call your function to retrieve weather information (e.g., calling weather API)
    weather_info = get_weather(parameters)
    
    # Send tool_response message
    send_tool_response(tool_call_id, weather_info)

# Function to retrieve weather information
def get_weather(parameters):
    # Here you would implement code to actually retrieve weather information
    # For the sake of example, let's assume we're just returning a hardcoded value
    return "60F"

# Send tool_response message
def send_tool_response(tool_call_id, weather_info):
    response_body = {
        "type": "tool_response",
        "tool_call_id": tool_call_id,
        "content": weather_info
    }
    
    # Make a POST request to send the tool_response message
    response = requests.post(RESPONSE_URL, json=response_body, headers=headers)
    
    if response.status_code != 200:
        print("Failed to send tool_response message. Status code:", response.status_code)

# Main function
if __name__ == "__main__":
    listen_for_tool_call()
