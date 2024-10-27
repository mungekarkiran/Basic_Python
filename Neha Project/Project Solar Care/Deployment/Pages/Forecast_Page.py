import streamlit as st
import pandas as pd
import pickle
from datetime import datetime, timedelta

# Load pre-trained models
def load_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

# Paths to saved models (update paths as needed)
temperature_model_path = 'models/temp_model.pkl'
dew_model_path = 'models/dew_model.pkl'
humidity_model_path = 'models/humidity_model.pkl'

temperature_model = load_model(temperature_model_path)
dew_model = load_model(dew_model_path)
humidity_model = load_model(humidity_model_path)

# Forecasting function
def forecast_next_24_hours(start_date):
    # format specification
    format = '%Y-%m-%d %H:%M:%S'
    forecast_dates = [start_date + timedelta(hours=i) for i in range(24)]
    start_date, end_date = forecast_dates[0].strftime(format), forecast_dates[-1].strftime(format)

    # Use models to make predictions
    temperature_forecast = temperature_model.predict(start=start_date, end=end_date)
    dew_forecast = dew_model.predict(start=start_date, end=end_date)
    humidity_forecast = humidity_model.predict(start=start_date, end=end_date)
        
    # Create a DataFrame with results
    forecast_data = pd.DataFrame({
        'DateTime': forecast_dates,
        'Temperature': round(temperature_forecast,2),
        'Dew': round(dew_forecast,2),
        'Humidity': round(humidity_forecast,2)
    })
    
    return forecast_data

def forecast_page():
    st.title("Solar Panel Care - 24 Hour Forecast")
    st.write("Use the trained models to forecast temperature, dew, and humidity for the next 24 hours.")

    # Get the user-provided date
    user_date = st.date_input("Select a starting date:")
    user_time = st.time_input("Select a starting time:")

    start_date = datetime.combine(user_date, user_time)

    if st.button("Forecast"):
        forecast_df = forecast_next_24_hours(start_date)
        st.write("Forecast for the next 24 hours:")
        st.write(forecast_df.set_index("DateTime"))

        # # Optionally plot the forecast
        st.line_chart(forecast_df.set_index("DateTime"))
