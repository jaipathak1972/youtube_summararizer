import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

# Prompt for summarization
prompt = (
    "You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video "
    "and providing the important summary in points within 250 words in English. The transcript text will be appended "
    "here it will be in Hindi or English but your response should be only in English: "
)

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        try:
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except:
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None

def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .main {
        background-color: black;
    }
    .stSlider {
        color: #4CAF50;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("YouTube Transcript to Detailed Notes Converter")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home"])

if page == "Home":
    st.header("Home")

    # YouTube video link input
    youtube_link = st.text_input("Enter YouTube Video Link:")

    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    # Slider for setting summary length (for future use)
    summary_length = st.slider("Summary Length (in words)", 50, 500, 250)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            if summary:
                st.markdown("## Detailed Notes:")
                st.write(summary)

st.sidebar.image("https://via.placeholder.com/150", caption="Image 1")
st.sidebar.image("https://via.placeholder.com/150", caption="Image 2")


