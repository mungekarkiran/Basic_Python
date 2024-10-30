import os
import pickle
import pandas as pd
import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Functions
def save_train_model(model, col):
    # Create folder if not exist
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)

    # Save trained model to folder
    model_path = os.path.join(model_dir, f'{col}_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    # st.success(f"Model for {col} is saved!")
    return model_path

def train_model(data, column=['temp', 'dew', 'humidity']): # , 'dew', 'humidity'
    # Convert 'datetime' to a datetime object
    data['datetime'] = pd.to_datetime(data['datetime'])

    # Set 'datetime' as the index
    data.set_index('datetime', inplace=True)

    model_paths = []
    for col in column:
        # Train/test split
        train_data, test_data = data[col][:-24], data[col][-24:]
        
        # Train ARIMA model
        model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24)).fit()
        
        # Save the models 
        model_paths.append(save_train_model(model, col))
        
        # Evaluate next 24 hours on test data
        evaluate_next_24_hours(model, train_data, test_data, col)
    
    # return set(model_paths)


def evaluate_next_24_hours(model, train_data, test_data, col):
    # Make prediction
    predictions = model.predict(start=len(train_data), end=len(train_data) + 23)
    # predictions = round(predictions, 2)

    data = pd.DataFrame({
        "datetime": test_data.index,
        "actual": test_data,
        "predicted": round(predictions, 2)
        })

    data = data.set_index("datetime")

    st.write(f"{col} Forecasting on Test data:")

    # Plot two lines on the same chart
    st.line_chart(data)
    

def home_page():
    st.title("Solar Panel Care Dashboard")
    st.write("Welcome to the Solar Panel Care Application!")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file with datetime, temperature, dew, and humidity data")

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.write(data.head())

        # Choose column to train on
        # column = st.selectbox("Select column to train on", data.columns)

        # Train model
        if st.button("Train Model"):
            with st.spinner("Training model, please wait..."):
                model_paths = train_model(data)
            st.success("Model training complete!")

        # # After training the model...
        # # if st.button("Forecast Next 24 Hours"):
        # forecast = forecast_next_24_hours(model)
        # st.write("Next 24-hour Forecast:")
        # st.write(forecast)