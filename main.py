import network
import urequests as requests
import machine
import random
import keys
import dht
import time

TOKEN = "BBUS-HMzHEIaVO6nXzuYZ6Q0o5FbZPeXreh"  # Put here your TOKEN
DEVICE_LABEL = "picowboard"                    # Assign the device label desired to be sent
VARIABLE_LABEL_TEMP = "temperature"            # Variable label for temperature
VARIABLE_LABEL_HUM = "humidity"                # Variable label for humidity
WIFI_SSID = keys.WIFI_SSID                     # Assign the SSID of your network
WIFI_PASS = keys.WIFI_PASS                     # Assign the password of your network
DELAY = 5                                      # Delay in seconds

# File path for CSV
csv_file = 'weather_power.csv'

# Function to initialize the CSV file with headers if it does not exist
def initialize_csv(file_path):
    try:
        # Check if the file exists and is not empty
        with open(file_path, 'r') as file:
            if file.read().strip() == '':  # If the file is empty
                raise OSError("File is empty")
    except OSError:
        print("Initializing CSV file...")
        try:
            with open(file_path, 'w') as file:
                file.write('timestamp,temperature,humidity,power_consumption\n')
            print("CSV file initialized.")
        except Exception as e:
            print(f"Failed to initialize CSV file: {e}")

# Function to append data to the CSV file
def append_to_csv(file_path, data):
    try:
        with open(file_path, 'a') as file:
            file.write(data + '\n')
            file.flush()  # Ensure data is written immediately
    except Exception as e:
        print(f"Failed to append data to CSV: {e}")

# Function for WiFi connection
def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('Connecting to network...')
        wlan.active(True)                       # Activate network interface
        wlan.config(pm=0xa11140)                # Set power mode to get WiFi power-saving off (if needed)
        wlan.connect(WIFI_SSID, WIFI_PASS)      # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            time.sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip

# Function to simulate power consumption reading
def read_power_consumption():
    # Simulate or read actual power consumption from a sensor
    return random.uniform(0.5, 2.0)  # Example range in kWh

# Function to get current timestamp formatted as a string
def get_timestamp():
    t = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5])

# Connect to the WiFi
connect()


tempSensor = dht.DHT11(machine.Pin(21))

# initialize_csv(csv_file)

while True:
    try:
        # Measure temperature and humidity
        tempSensor.measure()
        temperature = tempSensor.temperature()
        humidity = tempSensor.humidity()

        # Simulate reading power consumption
        power_consumption = read_power_consumption()

        # Get the current timestamp
        timestamp = get_timestamp()

        # Prepare data as a CSV row
        data = f"{timestamp},{temperature},{humidity},{power_consumption}"

        # Append the data to the CSV file
        append_to_csv(csv_file, data)

        # Print the sensor values
        print(f"{timestamp} - Temperature: {temperature}°C, Humidity: {humidity}%, Power Consumption: {power_consumption} kWh")

    except OSError as e:
        print("Failed to read sensor:", e)
    except Exception as e:
        print("Exception occurred:", e)

    # Wait before the next measurement
    time.sleep(DELAY)