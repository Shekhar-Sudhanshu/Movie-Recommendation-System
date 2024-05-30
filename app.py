import streamlit as st
import pandas as pd
import joblib
import wikipedia

st.set_page_config(
    page_title="Recommendation System",
    page_icon="🎬"
)

data = pd.read_csv("Dataset/dataset.csv")
data.dropna(inplace=True)


def get_recommendations(movie):
    movies = []
    similarity = joblib.load("model/similarity.pkl")
    index = data[data['title']==movie].index[0]
    suggestions = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vectors: vectors[1])
    for i in suggestions[0:10]:
        if(data.iloc[i[0]].title == movie): continue
        movies.append(data.iloc[i[0]].title)
    return movies

def get_movies():
    movies = []
    for i in data.index:
        movies.append(data['title'][i])
    return movies


about = st.sidebar.empty()
st.title("Movie Recommendation System")
st.sidebar.text("More Suggestions")

movie = st.selectbox(label="Select a Movie", options=get_movies())
btn = st.button("Suggest", type="primary")

if(btn):
    with st.spinner("Searching"):
        about.write(f"About {movie} \n\n {data[data['title']==movie].overview.values[0]}")
        suggestions = get_recommendations(movie)
        st.text("Recommended Movies")
        for i in suggestions[0:5]:
            with st.expander(i):
                st.write(f"Genre - {data[data['title']==i].genre.values[0]}")
                st.write(f"Release Date - {data[data['title']==i].release_date.values[0]}")
                st.write(f"About - {data[data['title']==i].overview.values[0]}")
                try:
                    page = wikipedia.page(i)
                    st.write(f"[Link]({page.url})")
                except:
                    st.write("")
                         
        j = 1
        for i in suggestions[5:]:
            st.sidebar.write(f"{j}. {i}")
            j+=1