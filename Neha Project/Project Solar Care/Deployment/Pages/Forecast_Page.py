import streamlit as st
import pandas as pd
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Load pre-trained models
def load_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)

# Paths to saved models (update paths as needed)
temperature_model_path = 'models/temp_model.pkl'
dew_model_path = 'models/dew_model.pkl'
humidity_model_path = 'models/humidity_model.pkl'

try:
    temperature_model = load_model(temperature_model_path)
    dew_model = load_model(dew_model_path)
    humidity_model = load_model(humidity_model_path)
except Exception as e:
    st.warning(f"Warning : 404 : Time series models not found.", icon=None)

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
        'temp': round(temperature_forecast,2), # Temperature
        'dew': round(dew_forecast,2), # Dew
        'humidity': round(humidity_forecast,2) # Humidity
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

        # Optionally plot the forecast
        st.line_chart(forecast_df.set_index("DateTime"))

        data = forecast_df.drop(["DateTime"], axis=1)

        classification_model_path = 'models/classification_model.pkl'
        try:
            classification_model = load_model(classification_model_path)
        except Exception as e:
            st.warning(f"Warning : 404 : Classification models not found.", icon=None)

        # Make prediction
        prediction = classification_model.predict(data)
        forecast_df['pre_label'] = prediction
        
        # Display the prediction result
        st.write("Prediction result: ")
        st.write(forecast_df.set_index("DateTime"))
        st.line_chart(forecast_df.set_index("DateTime"))

        # Pie Chart in Column 1        
        st.write("### Pie Chart of `Need to Clean` Distribution")
        pre_label_counts = forecast_df['pre_label'].value_counts()
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(pre_label_counts, labels=pre_label_counts.index, autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')  # Equal aspect ratio ensures that the pie chart is a circle.
        st.pyplot(fig_pie)
        
        # Final prediction
        mgs= ''
        if round((forecast_df['pre_label'].sum()/24)*100, 1) > 50 :
            msg = '### Your Solar Panel need to Clean.'
        else :
            msg = '### No need to Clean your Solar Panel.'
        st.write(msg)