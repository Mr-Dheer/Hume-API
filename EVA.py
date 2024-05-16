
#! Responding only once
#!config_id='ede9c815-c884-479a-b959-21b1db2f770b'
# ede9c815-c884-479a-b959-21b1db2f770b
import os
from hume import HumeVoiceClient, MicrophoneInterface
from dotenv import load_dotenv
import asyncio
import logging



# Configure logging
logging.basicConfig(level=logging.INFO)

async def main() -> None:
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

        # Start streaming EVI over your device's microphone and speakers 
        async with client.connect(config_id='ede9c815-c884-479a-b959-21b1db2f770b') as socket:
            await MicrophoneInterface.start(socket)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

asyncio.run(main())




# import os
# import asyncio
# import logging
# from dotenv import load_dotenv
# from hume import HumeVoiceClient, MicrophoneInterface

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# async def start_stream(socket):
#     try:
#         while True:
#             await MicrophoneInterface.start(socket)
#             await asyncio.sleep(0.1)  # Small sleep to prevent tight loop
#     except asyncio.CancelledError:
#         logging.info("Microphone task cancelled")

# async def main() -> None:
#     # Load environment variables from .env file
#     load_dotenv()

#     # Retrieve the Hume API key from the environment variables
#     HUME_API_KEY = os.getenv("HUME_API_KEY")
#     if not HUME_API_KEY:
#         logging.error("HUME_API_KEY environment variable is not set")
#         return

#     try:
#         # Connect and authenticate with Hume
#         client = HumeVoiceClient(HUME_API_KEY)

#         # Start streaming EVI over your device's microphone and speakers
#         async with client.connect() as socket:
#             # Start the microphone interface
#             mic_task = asyncio.create_task(start_stream(socket))

#             # Keep the main coroutine running indefinitely
#             while True:
#                 await asyncio.sleep(1)  # Keep the event loop running

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())
