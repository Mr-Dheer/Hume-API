from hume import HumeBatchClient
from hume.models.config import FaceConfig

client = HumeBatchClient('nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj')
file_path=[
    'AngryDataSet.zip'
]
config = FaceConfig()
job = client.submit_job(None, [config], files=file_path)

print(job)
print('Mein Bhaag Raha Hun Ruko Zara')

details= job.await_complete()
job.download_predictions('Predictions-2.json')
print('Predictions-2 Downloaded')

# Load the JSON data
import json

file_path = 'Predictions-2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Prepare to store the results
results = []

# Loop through each prediction
for prediction in data[0]['results']['predictions']:
    file_name = prediction['file']
    emotions = prediction['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions']
    
    # Sort emotions by score in descending order
    sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
    
    # Get the top 3 emotions
    top_3_emotions = sorted_emotions[:3]
    
    # Prepare data for each prediction
    prediction_result = {
        'file': file_name,
        'top_emotions': [
            {'name': emotion['name'], 'score': emotion['score']} for emotion in top_3_emotions
        ]
    }
    
    # Append to results list
    results.append(prediction_result)

# Write results to a new JSON file
output_file_path = 'AagyaPaaji Mein-3.json'
with open(output_file_path, 'w') as output_file:
    json.dump(results, output_file, indent=2)

print(f"Top emotions data written to '{output_file_path}'.")
