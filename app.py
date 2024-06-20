import pickle
import streamlit as st
import requests
import base64


# Function to add custom CSS for background
def add_background(image_file):
    with open( image_file, "rb" ) as f:
        data = f.read()
    encoded_image = base64.b64encode( data ).decode()

    st.markdown(
        f"""
        <style>
        body {{
            background-image: url(data:image/png;base64,{encoded_image});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp {{
            background: rgba(0, 0, 0, 0.5);  /* Optional: Adds a semi-transparent background to the main content for readability */
            border-radius: 10px;
            padding: 10px;
        }}
        .custom-header {{
            color: white;  /* Set the header color to white */
        }}
        .stText {{
            color: white !important;  /* Set st.text color to white */
        }}
        
                 </style>
        """,
        unsafe_allow_html=True
    )


# Call the function to add the background
add_background( "bg image 2.jpg" )

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c1b5181df730ca21c034c6b9ab30ee05&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.markdown('<h1 class="custom-header">Movie Recommender System</h1>', unsafe_allow_html=True)
movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.markdown('<h6 style="color:white;">Type or select a movie from the dropdown</h6>', unsafe_allow_html=True)
movie_list = movies['title'].values
selected_movie = st.selectbox("type",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0])
        statement = '<h6 style="color:white;">'+ recommended_movie_names[0]+'</h6>'
        st.markdown(statement, unsafe_allow_html=True)

    with col2:
        st.image(recommended_movie_posters[1])
        statement = '<h6 style="color:white;">' + recommended_movie_names[1] + '</h6>'
        st.markdown(statement, unsafe_allow_html=True)


    with col3:
        st.image(recommended_movie_posters[2])
        statement = '<h6 style="color:white;">' + recommended_movie_names[2] + '</h6>'
        st.markdown(statement, unsafe_allow_html=True)

    with col4:
        st.image(recommended_movie_posters[3])
        statement = '<h6 style="color:white;">' + recommended_movie_names[3] + '</h6>'
        st.markdown( statement, unsafe_allow_html=True )

    with col5:
        st.image(recommended_movie_posters[4])
        statement = '<h6 style="color:white;">' + recommended_movie_names[4] + '</h6>'
        st.markdown( statement, unsafe_allow_html=True )







