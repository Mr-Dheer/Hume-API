import streamlit as st
import pickle
import pandas as pd

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



def recommend(movie, similarity_matrix, df):
    if movie:  # Check if movie name is provided
        try:
            index = df[df['title'] == movie].index[0]
            distances = sorted(enumerate(similarity_matrix[index]), reverse=True, key=lambda x: x[1])

            for i in distances[1:6]:
                recommended_movie = df.iloc[i[0]].title
                similarity_score = i[1]
                st.subheader(f"{recommended_movie} (Cosine Similarity: {similarity_score:.3f})")
        except IndexError:
            st.error("Movie not found in the database. Please enter a valid movie name.")

def main():
    emotion = st.selectbox('Enter the emotion you are feeling',
    ('happy', 'angry', 'neutral', 'sad'),
    index=None
    )
    st.write(f'Selected Emotion :red[{emotion}]')
    
    if emotion not in ['happy', 'sad', 'angry', 'neutral']:
        return 
    
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
    st.write('Randomly Choosen Movies')
    
    for i in get_random_movie:
        st.write("- "+i)

    Random_movie = st.selectbox('Enter or choose a Movie',df_emotion['title'],index=None)

    if Random_movie:  # Check if movie name is provided
        st.write(f"Selected movie: :red[{Random_movie}]")
        st.subheader(':blue[Recommendations for the movie are below]', divider='rainbow')
        recommend(Random_movie, similarity_matrix, df_emotion)
    else:
        st.write("Please enter a movie name to get recommendations.")

main()


    
