import streamlit as st
from dotenv import load_dotenv
import os
import requests
from langchain.chat_models import init_chat_model


load_dotenv()

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not weather_api_key or not groq_api_key:
    st.error("API keys not found. Please set OPENWEATHER_API_KEY and GROQ_API_KEY in .env")
    st.stop()

llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)


st.set_page_config(page_title="Weather Summary", layout="centered")
st.title("🌦️ Weather Summary App")

city = st.text_input("Enter city name")

if st.button("Get Weather") and city.strip():

    with st.spinner("Fetching weather data..."):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)

    if response.status_code != 200:
        st.error(response.json().get("message", "Error fetching weather"))
    else:
        data = response.json()

      
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

      
        st.subheader(f"📍 Weather in {city.title()}")
        st.metric("🌡️ Temperature (°C)", temperature)
        st.metric("💧 Humidity (%)", humidity)
        st.metric("🌬️ Wind Speed (m/s)", wind_speed)

    
        prompt = f"""
        The current weather in {city} is:
        - Temperature: {temperature} °C
        - Humidity: {humidity} %
        - Wind Speed: {wind_speed} m/s

        Explain this weather in simple English.
        """

        with st.spinner("Generating explanation..."):
            explanation = llm.invoke(prompt)

        st.subheader("🧠 Simple Explanation")
        st.write(explanation.content)

elif city == "":
    st.info("Please enter a city name.")