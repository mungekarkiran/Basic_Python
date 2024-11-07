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
    print("Could not connect to Arduino. Check port and try again.")
    # exit()

# Function to read sensor data
# def read_sensor_data():
#     if arduino.in_waiting > 0:  # Check if there's data waiting to be read
#         try:
#             data = arduino.readline().decode().strip()  # Read and decode the data
#             data1 = [float(item.strip()) for item in data.split('|')]
#             print("Sensor Value:", data1, [data1[:-1]])

#             classification_model_path = 'models/classification_model.pkl'
#             try:
#                 classification_model = load_model(classification_model_path)
#             except Exception as e:
#                 st.warning(f"Warning : 404 : Classification models not found.", icon=None)

#             # Make prediction
#             prediction = classification_model.predict([data1[:-1]])
#             if prediction[0] == 0:
#                 arduino.write(b'0')
#             else:
#                 arduino.write(b'1')
#                 st.write("Signal send")
#         except Exception as e:
#             # st.warning("Error reading data:", e)
#             pass

def classification_page():

    st.title("Solar Panel Care - Maintenance Classification")
    st.write("Use the trained models to send signal to clean Solar Panel.")

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Place a button in each column
    with col1:
        # if st.button("Button 1"):
        #     st.write("Button 1 clicked")

        if st.button("Maintenance Classification"):
            # Main loop to read data continuously
            try:
                while True:
                    # read_sensor_data()
                    if arduino.in_waiting > 0:  # Check if there's data waiting to be read
                        try:
                            data = arduino.readline().decode().strip()  # Read and decode the data
                            data1 = [float(item.strip()) for item in data.split('|')]
                            print("Sensor Value:", data1, [data1[:-1]])

                            classification_model_path = 'models/classification_model.pkl'
                            try:
                                classification_model = load_model(classification_model_path)
                            except Exception as e:
                                st.warning(f"Warning : 404 : Classification models not found.", icon=None)

                            # Make prediction
                            prediction = classification_model.predict([data1[:-1]])
                            if prediction[0] == 0:
                                arduino.write(b'0')
                            else:
                                arduino.write(b'1')
                                st.write(f"Signal send : {data1}")
                                break
                        except Exception as e:
                            # st.warning("Error reading data:", e)
                            pass
                    time.sleep(5)  # Adjust as needed for your application

            except KeyboardInterrupt:
                st.warning("\nProgram interrupted by user.")
            
            # # Close the serial connection
            # finally:
            #     arduino.close()
            #     print("Disconnected from Arduino.")

    with col2:
        # if st.button("Button 2"):
        #     st.write("Button 2 clicked")
        
        if st.button("Manual Cleaning"):
            arduino.write(b'1')
            st.write(f"Manual Signal send ")

    with col3:
        if st.button("Restart"):
            # st.write("Restart")
            ...

    
 

    
