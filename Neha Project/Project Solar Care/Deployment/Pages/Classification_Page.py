import streamlit as st
import pandas as pd
import pickle
import serial
import time

# Load pre-trained models
def load_model(model_path):
    with open(model_path, 'rb') as file:
        return pickle.load(file)
    
# Replace 'COM3' with your Arduino's serial port
arduino_port = 'COM5'
baud_rate = 9600  # Same baud rate as in the Arduino code

# Establish serial connection
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=0.1)
    time.sleep(2)  # Wait for the connection to initialize
    print("Connected to Arduino!")
except serial.SerialException:
    st.warning("Could not connect to Arduino. Check port and try again.")
    # exit()

# Function to read sensor data
def read_sensor_data():
    val = []
    if arduino.in_waiting > 0:  # Check if there's data waiting to be read
        try:
            data = arduino.readline().decode().strip()  # Read and decode the data
            data1 = [float(item.strip()) for item in data.split('|')]
            print("Sensor Value:", data1)

            classification_model_path = 'models/classification_model.pkl'
            try:
                classification_model = load_model(classification_model_path)
            except Exception as e:
                st.warning(f"Warning : 404 : Classification models not found.", icon=None)

            # Make prediction
            prediction = classification_model.predict(data)
            if prediction[0] == 0:
                arduino.write(b'0')
            else:
                arduino.write(b'1')
        except Exception as e:
            st.warning("Error reading data:", e)

def classification_page():

    if st.button("Maintenance Classification"):
        # Main loop to read data continuously
        try:
            while True:
                read_sensor_data()
                time.sleep(3)  # Adjust as needed for your application
        except KeyboardInterrupt:
            st.warning("\nProgram interrupted by user.")

        # Close the serial connection
        finally:
            arduino.close()
            print("Disconnected from Arduino.")
 

