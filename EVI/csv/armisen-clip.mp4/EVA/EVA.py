
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
#

        # Start streaming EVI over your device's microphone and speakers 
        async with client.connect(config_id="dffb3e2f-a11f-4096-879e-63bb7e79fb9d") as socket:
            await MicrophoneInterface.start(socket)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

asyncio.run(main())