import streamlit as st
import pandas as pd
import difflib
import pickle

# Load dataset from Google Drive
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1cCkwiVv4mgfl20ntgY3n4yApcWqqZQe6'
    df = pd.read_csv(url)
    return df

# Load similarity pickle
@st.cache_data
def load_similarity():
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    return similarity

df = load_data()
similarity = load_similarity()

# --- Premium Purple UI Styling ---
st.markdown("""
    <style>
        html, body, [class*="st-"] {
            background: linear-gradient(135deg, #1B0036, #3D0D5E);
            color: #F2E7FE;
            font-family: 'Poppins', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #E0B3FF;
        }

        .stTextInput > div > div > input {
            background-color: #2C1A40;
            color: #FFFFFF;
            border: 1px solid #9145B6;
            border-radius: 8px;
            padding: 10px;
        }

        .stButton > button {
            background-color: #9A44FF;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #BB6BFF;
            color: #000;
            transform: scale(1.03);
        }

        .stMarkdown h3 {
            color: #DDB6FF;
            font-size: 24px;
            margin-top: 20px;
        }

        .stMarkdown p {
            font-size: 16px;
            color: #F8EBFF;
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- App Content ---
st.title("🎬 Movie Recommendation System")
st.markdown("### Find Your Next Favorite Film 🎥")
st.markdown("Enter a movie name you like, and get 30 similar recommendations, powered by content-based filtering.")

movie_name = st.text_input("🔎 Enter Your Favourite Movie Name")

if st.button("✨ Get Recommendations"):
    all_titles = df["title"].tolist()
    close_matches = difflib.get_close_matches(movie_name, all_titles)

    if close_matches:
        close_match = close_matches[0]
        matched_rows = df[df.title == close_match]

        if not matched_rows.empty:
            index = matched_rows["index"].values[0]
            similarity_scores = list(enumerate(similarity[index]))
            sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

            st.markdown("### 🎯 Recommended Movies for You:")
            i = 1
            for movie in sorted_scores:
                index = movie[0]
                title = df[df.index == index]["title"].values[0]
                if i <= 30:
                    st.markdown(f"**{i}.** {title}")
                    i += 1
        else:
            st.error("Movie not found in dataset.")
    else:
        st.error("No close match found. Please try a different title.")