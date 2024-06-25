import asyncio
import websockets
import json
import cv2  # OpenCV for capturing frames from webcam or video file
import base64  # for base64 encoding of image data
import time

async def connect_to_hume_websocket(api_key):
    uri = "wss://api.hume.ai/v0/stream/models"
    
    # Prepare the WebSocket headers with API key
    headers = {
        "X-Hume-Api-Key": api_key
    }
    
    try:
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            print("Connected to Hume AI WebSocket")
            
            # OpenCV setup to capture frames from webcam
            cap = cv2.VideoCapture(1)  # Change to your desired camera index or video file path
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set lower resolution if needed
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            font = cv2.FONT_HERSHEY_COMPLEX
            
            while cap.isOpened():
                start_time = time.time()
                
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Encode frame as JPEG
                _, encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                # Convert to base64 string
                frame_base64 = base64.b64encode(encoded).decode('utf-8')
                
                # Prepare JSON message with frame data for face expression analysis
                message = {
                    "models": {
                        "face": {}
                    },
                    "data": frame_base64
                }
                
                try:
                    # Send JSON message to WebSocket
                    await websocket.send(json.dumps(message))
                    
                    # Receive and parse JSON response data
                    json_response_data = await websocket.recv()
                    response = json.loads(json_response_data)
                    
                    # Getting Emotions
                    emotions = response['face']['predictions'][0]['emotions']
                    # Sort emotions by score in descending order
                    sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)

                    # Get the top 3 emotions
                    top_3_emotions = sorted_emotions[:3]

                    # Print the top 3 emotions
                    for emotion in top_3_emotions:
                        print(f"Emotion: {emotion['name']}, Score: {emotion['score']}")

                    # Display top 3 emotions on the frame
                    for i, emotion in enumerate(top_3_emotions):
                        text = f"{emotion['name']}: {emotion['score']:.2f}"
                        cv2.putText(frame, text, (10, 50 + i*30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed")
                    break
                
                # Display the frame in a window
                cv2.imshow('Camera Feed', frame)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                
                # Calculate and print frame processing time
                end_time = time.time()
                print("Frame processing time:", end_time - start_time)
            
            cap.release()
            cv2.destroyAllWindows()
    
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Failed to connect: {e}")

async def main():
    # Replace with your actual API key
    api_key = "nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj"
    
    await connect_to_hume_websocket(api_key)

# Run the main function
asyncio.run(main())
