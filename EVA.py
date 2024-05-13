

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
        async with client.connect(config_id='b6a03472-09b8-4fc9-b528-1651fea6231f') as socket:
            await MicrophoneInterface.start(socket)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

asyncio.run(main())
