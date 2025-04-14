import streamlit as st
from google.cloud import aiplatform
import google.generativeai as genai
import os

# Initialize Vertex AI
aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_LOCATION"))

# Gemini setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def get_sentiment(text):
    """Gets sentiment form Vertex AI's text sentiment analysis model."""
    endpoint = aiplatform.Endpoint(os.environ.get("VERTEX_ENDPOINT_ID"))
    instances = [{"content": text}]
    prediction = endpoint.predict(instances=instances)
    sentiment_score = prediction.predictions[0]["sentiment"]
    return sentiment_score

def get_gemini_explanation(text):
    """Gets sentiment explanation from Gemini."""
    prompt = f"Explain the sentiment of the following text: '{text}'"
    try: 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting explanation from Gemini: {e}"
    
    st.title("Text Sentiment Analysis with Gemini")

    text_input = st.text_area("Enter text for sentiment analysis:")

    if st.button("Analyze"):
        if text_input:
            sentiment_score = get_sentiment(text_input)
            st.write(f"Sentiment Score: {sentiment_score}")

            if sentiment_score > 0.5:
                st.write("Positive Sentiment")
            elif sentiment_score < -0.5:
                st.write("Negative Sentiment")
            else:
                st.write("Neutral Sentiment")

            if st.checkbox("Get Gemini Explanation"):
                explanation = get_gemini_explanation(text_input)
                st.write(f"Gemini Explanation: {explanation}")
    else: 
        st.write("Please enter some text.")
