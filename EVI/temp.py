import os
from hume import HumeVoiceClient, MicrophoneInterface
from dotenv import load_dotenv
import asyncio
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

# Mock implementation of get_weather function
def get_weather(location, format):
    # This is where you would call a real weather API
    # For now, we'll just return a hardcoded response
    return "The weather in {} is 72F.".format(location)

async def handle_tool_call(socket, tool_call):
    logging.info(f"Handling tool call: {tool_call}")

    # Ensure tool_call is a dictionary
    if isinstance(tool_call, dict):
        if tool_call.get('name') == 'getStupidWeather':
            parameters = tool_call.get('parameters', {})
            logging.info(f"Tool call parameters: {parameters}")

            # Ensure parameters is a dictionary
            if isinstance(parameters, str):
                parameters = json.loads(parameters)
            
            logging.info(f"Parsed parameters: {parameters}")

            location = parameters.get('location')
            format = parameters.get('format')
            
            if not location or not format:
                logging.error(f"Invalid parameters for getStupidWeather: {parameters}")
                return
            
            # Call your function to get weather information
            weather_info = get_weather(location, format)
            
            # Prepare and send tool response
            tool_response = {
                "type": "tool_response",
                "tool_call_id": tool_call["tool_call_id"],
                "content": weather_info
            }
            
            # Send the tool response to EVI
            await socket.send_json(tool_response)
        else:
            logging.error("Tool call name is not 'getStupidWeather'")
    else:
        logging.error("tool_call is not a dictionary")

async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the Hume API key from the environment variables
    HUME_API_KEY = os.getenv("HUME_API_KEY")
    if not HUME_API_KEY:
        logging.error("HUME_API_KEY environment variable is not set")
        return

    try:
        # Connect and authenticate with Hume
        client = HumeVoiceClient(HUME_API_KEY)

        # Start streaming EVI using the specified configuration ID
        config_id = "b5f295e1-1dff-44a1-90a7-0d8456959a26"  # Replace with your actual config ID for 'testing-3'
        async with client.connect(config_id=config_id) as socket:
            logging.info(f"Connected to EVI with config ID: {config_id}")

            # Listen for messages from EVI
            async for message in socket:
                logging.info(f"Received message: {message}")
                
                # Parse the message from JSON string to dictionary
                try:
                    message = json.loads(message)
                except json.JSONDecodeError:
                    logging.error(f"Failed to decode JSON message: {message}")
                    continue
                
                if isinstance(message, dict) and 'type' in message:
                    if message['type'] == 'tool_call':
                        await handle_tool_call(socket, message)
                    elif message['type'] == 'assistant_message':
                        logging.info(f"Assistant message from EVI: {message['message']['content']}")
                    else:
                        logging.info(f"Received unknown message type: {message}")
                else:
                    logging.error(f"Received non-dictionary message: {message}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
