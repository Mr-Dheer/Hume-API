import json
from hume import HumeBatchClient
from hume.models.config import FaceConfig

client = HumeBatchClient('nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj')
file_path=[
    'AngryCorrectDataSet.zip'
]
config = FaceConfig()
job = client.submit_job(None, [config], files=file_path)

print(job)
print('Mein Bhaag Raha Hun Ruko Zara')

details= job.await_complete()
job.download_predictions('PredictionsCorrectDataSet.json')
print('PredictionsCorrectDataSet Downloaded')



# Load the JSON data
file_path = 'PredictionsCorrectDataSet.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Prepare to store the results and errors
results = []

# Loop through each prediction
for prediction in data[0]['results']['predictions']:
    file_name = prediction['file']
    prediction_result = {
        'file': file_name,
        'top_emotions': []
    }
    
    # Check if grouped_predictions exist and are not empty
    if 'grouped_predictions' in prediction['models']['face'] and prediction['models']['face']['grouped_predictions']:
        emotions = prediction['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions']
        
        # Sort emotions by score in descending order
        sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
        
        # Get the top 3 emotions
        top_3_emotions = sorted_emotions[:3]
        
        # Check if top 3 emotions are empty
        if not top_3_emotions:
            # Add error message
            prediction_result['error_message'] = f"No emotions detected for image: {file_name}"
            print(f"Error: No emotions detected for image: {file_name}")
        else:
            # Prepare data for each prediction
            prediction_result['top_emotions'] = [{'name': emotion['name'], 'score': emotion['score']} for emotion in top_3_emotions]
    else:
        # Add error message
        prediction_result['error_message'] = f"Issue with image: {file_name}"
        print(f"Error: Issue with image: {file_name}")

    # Append the result (including potential error_message) to results list
    results.append(prediction_result)

# Write results to a new JSON file
output_file_path = 'AakhriHai-2.json'
with open(output_file_path, 'w') as output_file:
    json.dump(results, output_file, indent=2)

print(f"Results (including errors) written to '{output_file_path}'.")



