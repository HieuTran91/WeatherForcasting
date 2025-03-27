import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

st.title(" Weather Forecast Dashboard")

weather_model = joblib.load("model/weather_model.pkl")
temp_model = joblib.load("model/temperature_model.pkl")

st.sidebar.header("Input Parameters")
hour = st.sidebar.slider("Hour", 0, 23, 12)
day = st.sidebar.selectbox("Day of Week", list(range(7)))

input_data = pd.DataFrame([[hour, day, 30.0]], columns=["hour", "day", "temperature_celsius"])
pred_temp = temp_model.predict(input_data)[0]
pred_weather = weather_model.predict(input_data)[0]

st.write(f"###  Forcasting:")
st.write(f"- Temperature: **{pred_temp:.2f} °C**")
st.write(f"- Have rain: {' Yes' if pred_weather[0] else ' NO'}")
st.write(f"- Have cloud: {' Yes' if pred_weather[1] else ' NO'}")
