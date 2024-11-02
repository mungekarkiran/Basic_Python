import serial
import time

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
    exit()

# Function to read sensor data
def read_sensor_data():
    val = []
    if arduino.in_waiting > 0:  # Check if there's data waiting to be read
        try:
            data = arduino.readline().decode().strip()  # Read and decode the data
            # print("Sensor Value:", data)
            # print("Sensor Value:", data.split('|'))
            data1 = [float(item.strip()) for item in data.split('|')]
            print("Sensor Value:", data1)
            # if len(data.split(':')) == 2:
                # print("Sensor Value:", data)
                # print("Sensor Value:", data.split(':'))
                # val.append(data.split(':')[-1])
            # print(val)
        except Exception as e:
            print("Error reading data:", e)

# Main loop to read data continuously
try:
    while True:
        read_sensor_data()
        time.sleep(.01)  # Adjust as needed for your application
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Close the serial connection
finally:
    arduino.close()
    print("Disconnected from Arduino.")
