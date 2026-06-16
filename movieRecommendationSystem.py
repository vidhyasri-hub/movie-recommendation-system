import streamlit as st
from dataProcessing import RecommendationEngine
from visualizations import plot_recommendations

st.set_page_config(page_title="Movie Match 2024", layout="wide")

@st.cache_resource
def init_engine():
    print("Points to the data folder")
    return RecommendationEngine('data/imdb_2024_movies.csv')

st.title("🎬 2024 Movie Recommender")
st.write("Find movies based on plot similarity using NLP.")

try:
    engine = init_engine()
    print("Recommendation engine initialized successfully.")

    user_query = st.text_area("Enter a storyline or keywords:", height=150)
    print(f"User input received: {user_query[:100]}...")  # Print the first 100 characters of user input for debugging

    if st.button("Get Recommendations"):
        if user_query:
            recs = engine.get_recommendations(user_query)
            
            if not recs:
                st.error("No matches found. Try different keywords.")
            else:
                for i, movie in enumerate(recs, 1):
                    with st.expander(f"{i}. {movie['name']} (Match: {movie['score']:.2%})"):
                        st.write(f"**Plot:** {movie['plot']}")
                        st.progress(float(movie['score']))
                fig = plot_recommendations(recs)
                st.pyplot(fig)
        else:
            st.warning("Please enter some text first.")

except Exception as e:
    st.error(f"Please ensure you have run dataScraper.py first. Error: {e}")