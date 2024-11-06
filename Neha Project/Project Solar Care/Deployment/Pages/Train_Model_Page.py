import os
import pickle
import pandas as pd
import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX
# For classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score

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

    # Train classification model
    classification_data = data[column]
    train_classification_model(classification_data)

def train_classification_model(classification_data):
    # Data generation
    classification_data = data_generation(classification_data)

    # train_test_split 80/20
    X, y = classification_data.drop(['label'], axis = 1),  classification_data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

    # Model initialization
    rf_Classifier = RandomForestClassifier()

    # train model
    rf_Classifier.fit(X_train, y_train)

    # test model
    y_pred = rf_Classifier.predict(X_test)

    # model evalution
    st.write("Accuracy_score:", round((accuracy_score(y_test, y_pred))*100,2),'%')
    st.write("Loss:", round((1-accuracy_score(y_test, y_pred))*100,2),'%')
    st.write("Cohen_kappa_score:", round((cohen_kappa_score(y_test, y_pred))*100,2),'%')
    
    # save model
    save_train_model(rf_Classifier, 'classification')

def data_generation(data):
    data['temp_rule'] = data['temp'].apply(lambda row: 1 if row >= 30 else 0)
    data['dew_rule'] = data['dew'].apply(lambda row: 1 if row > 25 else 0)
    data['humidity_rule'] = data['humidity'].apply(lambda row: 1 if row < 80 else 0)
    data['binary_rule'] = [str(data['temp_rule'][i]) + str(data['dew_rule'][i]) + str(data['humidity_rule'][i]) for i in range(len(data))]
    data['value_rule'] = [data['temp_rule'][i] + data['dew_rule'][i] + data['humidity_rule'][i] for i in range(len(data))]
    data['label'] = data['value_rule'].apply(lambda row: 1 if row >= 2 else 0)

    return data[['temp', 'dew', 'humidity', 'label']]

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
                train_model(data)
            st.success("Model training complete!")