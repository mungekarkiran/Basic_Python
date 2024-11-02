import serial
import time

# Replace 'COM3' with your Arduino's serial port
arduino_port = 'COM5'
baud_rate = 9600  # Must match the Arduino baud rate

# Establish serial connection
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for the connection to initialize
    print("Connected to Arduino!")
except serial.SerialException:
    print("Could not connect to Arduino. Check port and try again.")
    exit()

# Function to turn LED on or off
def control_led(state):
    if state == "on":
        arduino.write(b'1')  # Send '1' to turn on LED
        print("LED turned ON")
    elif state == "off":
        arduino.write(b'0')  # Send '0' to turn off LED
        print("LED turned OFF")
    else:
        print("Invalid state. Use 'on' or 'off'.")

# Example usage
try:
    while True:
        command = input("Enter 'on' to turn on the LED, 'off' to turn it off, or 'exit' to quit: ").strip().lower()
        if command == "exit":
            print("Exiting...")
            break
        control_led(command)
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")

# Close the serial connection
finally:
    arduino.close()
    print("Disconnected from Arduino.")
