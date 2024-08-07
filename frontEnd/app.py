import nbimporter
import streamlit as st
import pickle
import pandas as pd
from hume import HumeBatchClient
from hume.models.config import FaceConfig
import json
import requests
import time


#! Imported tmdb-api functions from another notebook
from tmdb_api import *


# Load DataFrame
df_happy = pickle.load(open('df_happy.pkl', 'rb'))
df_angry = pickle.load(open('df_angry.pkl', 'rb'))
df_sad = pickle.load(open('df_sad.pkl', 'rb'))
df_neutral = pickle.load(open('df_neutral.pkl', 'rb'))

# Load Similarity Cosine
similarity_happy = pickle.load(open('similarity_happy.pkl', 'rb'))
similarity_angry = pickle.load(open('similarity_angry.pkl', 'rb'))
similarity_sad = pickle.load(open('similarity_sad.pkl', 'rb'))
similarity_neutral = pickle.load(open('similarity_neutral.pkl', 'rb'))

st.title('Movie Recommender System')




# Initialize Hume API
client = HumeBatchClient('nvfkalYcOQpX7gElUYAGjpAbHyLvVzQSGJRupal2cCGTMrSj')

# Streamlit camera input to capture image
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # Convert the image file buffer to bytes
    bytes_data = img_file_buffer.getvalue()

    # Save the captured image to a file (Hume API requires a file path)
    with open('captured_image.jpg', 'wb') as f:
        f.write(bytes_data)

    # Hume API call to analyze the image
    file_path = ['captured_image.jpg']
    config = FaceConfig()
    job = client.submit_job(None, [config], files=file_path)

    # Wait for the job to complete and download the predictions
    details = job.await_complete()
    job.download_predictions('emotions.json')

    # Load the JSON data from the predictions file
    with open('emotions.json', 'r') as file:
        data = json.load(file)

    # Process the results
    results = []
    for prediction in data[0]['results']['predictions']:
        file_name = prediction['file']
        prediction_result = {'file': file_name, 'top_emotions': []}

        if 'grouped_predictions' in prediction['models']['face'] and prediction['models']['face']['grouped_predictions']:
            emotions = prediction['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions']
            sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
            top_emotions = sorted_emotions[:1]

            if not top_emotions:
                prediction_result['error_message'] = f"No emotions detected for image: {file_name}"
            else:
                prediction_result['top_emotions'] = [{'name': emotion['name'], 'score': emotion['score']} for emotion in top_emotions]
        else:
            prediction_result['error_message'] = f"Issue with image: {file_name}"

        results.append(prediction_result)

    # Display the results
    for result in results:
        #! Name of the file - Image
        # st.write(f"Name of the file is - {result['file']}")
        if 'error_message' in result:
            st.write(result['error_message'])
        else:
            for emotion in result['top_emotions']:
                detected_emotion = emotion['name']
                detected_emotion_score = emotion['score']
                #! Name of the emotion and the Score
                # st.subheader(f"It seems like the Emtion you are feeling is -  :red[{emotion['name']}]")
                # st.subheader(f"I can say this with - :red[{emotion['score']* 100:.0f}%] accuracy ")

    # Write results to a new JSON file (optional)
    output_file_path = 'captured_image_top_emotions.json'
    with open(output_file_path, 'w') as output_file:
        json.dump(results, output_file, indent=2)

    def map_emotion_to_category(detected_emotion):
        anger = ['Anger']
        happy = ['Joy', 'Amusement', 'Excitement', 'Interest', 'Awe']
        sad = ['Pain', 'Distress', 'Fear', 'Sadness', 'Disappointment']
        neutral = ['Calmness', 'Concentration', 'Boredom', 'Confusion', 'Doubt']

        if detected_emotion in anger:
            return 'angry'
        elif detected_emotion in happy:
            return 'happy'
        elif detected_emotion in sad:
            return 'sad'
        elif detected_emotion in neutral:
            return 'neutral'
        else:
            return 'Emotion not found'

    # Example usage:
    category = map_emotion_to_category(detected_emotion)
    #! Name of emotion categorty it falls in 
    # st.write(f"The detected emotion :red['{detected_emotion}'] falls under the category: :red[{category}]")

    def recommend(movie, similarity_matrix, df):
        if movie:  # Check if movie name is provided
            try:
                index = df[df['title'] == movie].index[0]
                distances = sorted(enumerate(similarity_matrix[index]), reverse=True, key=lambda x: x[1])

                for i in distances[1:6]:
                    recommended_movie = df.iloc[i[0]].title
                    movie_id = df.iloc[i[0]].movie_id
                    # st.write(recommended_movie)
                    similarity_score = i[1]
                    st.subheader(f"{recommended_movie}")
                    overview_movie = overview(movie_id)
                    trailer_movie = trailer(movie_id)
                    poster_movie = poster(movie_id)
                    review_movie = reviews(movie_id)
                    details_movie = detailsMovie(movie_id)

                    column1, column2 = st.columns([4,9])

                    with column1:
                        # st.write(overview_movie)
                        st.image(poster_movie)
                    with column2:
                        st.link_button('Trailer', trailer_movie)
                        
                        with st.expander('Movie Details'):
                            # Define columns for better spacing
                            col1, col2 = st.columns([1, 3])
                            
                            for i, detail in enumerate(details_movie):
                                with col1:
                                    st.markdown(f"**{list(detail.keys())[0]}:**")  # Key (only one per dictionary)
                                    if i< len(details_movie) -1 :
                                        st.markdown('---') 
                                with col2:
                                    st.markdown(f"   {list(detail.values())[0]}")  # Value (only one per dictionary)
                                    if i< len(details_movie) -1 :
                                        st.markdown('---')  # Adds a horizontal line for separation

                                
                        with st.expander('Overview'):
                            st.write(overview_movie)
                        with st.expander('Review'):
                            for index, i in enumerate(review_movie):
                                st.markdown(f"### Review {index + 1}")
                                st.write(i)
                            st.markdown("---")  # Adds a horizontal line between reviews


                    #! To get the cosine similarity
                    # st.subheader(f"{recommended_movie} (Cosine Similarity: {similarity_score:.3f})")
            except IndexError:
                st.error("Movie not found in the database. Please enter a valid movie name.")  

    def main(emotion):
        if emotion not in ['happy', 'sad', 'angry', 'neutral']:
            return st.error('Emotion not able to detect')

        if emotion == 'happy':
            similarity_matrix = similarity_happy
            df_emotion = df_happy

        elif emotion == 'angry':
            similarity_matrix = similarity_angry
            df_emotion = df_angry

        elif emotion == 'neutral':
            similarity_matrix = similarity_neutral
            df_emotion = df_neutral

        elif emotion == 'sad':
            similarity_matrix = similarity_sad
            df_emotion = df_sad

        get_random_movie = df_emotion['title'].sample(n=5, random_state=42)
        st.subheader(f'These are some of the movies you might like based on :red[{emotion}] emotion you are feeling')

        
        selected_movie = None
        for i in get_random_movie:
            if st.button(i):
                selected_movie = i
                st.write(f'You selected: {selected_movie}')
        #! Display random movies 
        # for i in get_random_movie:
        #     st.write("- " + i)
        
        st.subheader('You can also search for the movies I can make Recommendations based on that')

        Random_movie = st.selectbox('Enter or Choose a Movie', df_emotion['title'], index=None)

        if Random_movie:  # Check if movie name is provided
            st.write(f"Selected movie: {Random_movie}")
            st.subheader('Recommendations for the movie are below', divider='rainbow')
            recommend(Random_movie, similarity_matrix, df_emotion)
        else:
            st.write("Please enter a movie name to get recommendations.")

    main(category)
