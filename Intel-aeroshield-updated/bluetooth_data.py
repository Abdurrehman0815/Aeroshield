import serial
import pandas as pd
import time

# Replace 'COMx' with the actual port (e.g., 'COM5' or '/dev/ttyUSB0' on Linux)
bluetooth_port = 'COM10'  # Change this to your Bluetooth COM port
baud_rate = 9600  # Same baud rate as in the Arduino code
timeout = 2  # Timeout for serial read

# Initialize serial connection
ser = serial.Serial(bluetooth_port, baud_rate, timeout=timeout)

# Create an empty DataFrame to store the data
columns = ['Time (ms)', 'CO2 (ppm)', 'NH3 (ppm)', 'VOC (ppm)']
data_df = pd.DataFrame(columns=columns)

# Function to read from the Bluetooth serial port and process the data
def read_from_bluetooth():
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(line)
            data_values = line.split(',')  # Split CSV-like data from Arduino
            if len(data_values) == 4:  # Ensure we have 4 values (Time, CO2, NH3, VOC)
                # Append the data to the DataFrame
                new_data = pd.DataFrame([data_values], columns=columns)
                global data_df
                data_df = pd.concat([data_df, new_data], ignore_index=True)
    except Exception as e:
        print(f"Error reading from Bluetooth: {e}")

# Run the data collection process
print("Collecting data from Bluetooth... Press Ctrl+C to stop.")
try:
    while True:
        read_from_bluetooth()
        time.sleep(2)  # Delay between readings (same as Arduino delay)
except KeyboardInterrupt:
    print("\nData collection stopped.")

# Save the collected data to an Excel file
excel_filename = 'sensor_data.xlsx'
data_df.to_excel(excel_filename, index=False)
print(f"Data saved to {excel_filename}")
