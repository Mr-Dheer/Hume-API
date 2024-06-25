# from hume import HumeBatchClient
# from hume.models.config import FaceConfig

# client = HumeBatchClient("nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj")
# filepaths = [
#     "faces.zip",
# ]
# config = FaceConfig()
# job = client.submit_job(None, [config], files=filepaths)

# print(job)
# print("Running...")

# details = job.await_complete()
# job.download_predictions("predictions.json")
# print("Predictions downloaded to predictions.json")

import json

# Load the JSON data
file_path = 'predictions.json'
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Extract the emotions and their scores
emotions = json_data[0]['results']['predictions'][0]['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions']

# Sort emotions by score in descending order
sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)

# Get the top 3 emotions
top_3_emotions = sorted_emotions[:3]

# Print the top 3 emotions
for emotion in top_3_emotions:
    print(f"Emotion: {emotion['name']}, Score: {emotion['score']}")
