from flask import Flask, render_template, jsonify
from sense_emu import SenseHat
import json
import time

#from setuptools import setup

app = Flask (__name__)
sense = SenseHat()

# Define the temperature and humidity thresholds
TEMP_THRESHOLD = 40  # Threshold temperature in Celsius
HUMIDITY_THRESHOLD = 90  # Threshold humidity in percentage

@app.route('/')
def index():
       temperature = sense.get_temperature()
       humidity = sense.get_humidity()
       warning = check_and_display_warning(temperature, humidity)  # Implement this function to check warning conditions
       data = {
           'temperature': temperature,
           'humidity': humidity,
           'warning': warning
       }
       return json.dumps(data)
    
try:
         temperature = sense.get_temperature()
         humidity = sense.get_humidity()
         print("Temperature: {}°C".format(temperature))
         print("Humidity: {}%".format(humidity))
except Exception as e:
         print("An error occurred:", e)
         
# Function to check for warnings and update the web interface and Sense emulator
def check_and_display_warning():
    # Get current temperature and humidity readings
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()

    # Check if temperature or humidity exceeds thresholds
    if temperature > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
        # Construct the warning message
        warning_message = "WARNING: "

        if temperature > TEMP_THRESHOLD:
            warning_message += f"Temperature ({temperature:.2f}°C) exceeds {TEMP_THRESHOLD}°C. "
        if humidity > HUMIDITY_THRESHOLD:
            warning_message += f"Humidity ({humidity:.2f}%) exceeds {HUMIDITY_THRESHOLD}%. "
        
        # Display warning message on the web interface (replace this with your implementation)
        update_warning_message_on_web(warning_message)

        # Display warning message on the Sense emulator
        sense.show_message(warning_message, text_colour=[255, 0, 0])  # Red text

    else:
        # No warning, clear any existing messages on the Sense emulator
        sense.clear()
        

# Function to update warning message on the web interface (replace this with your implementation)
def update_warning_message_on_web(warning_message):
    print("Updating warning message on the web interface:", warning_message)


# Main loop to continuously monitor and display warnings
try:
    while True:
        check_and_display_warning()
        # Wait for a certain interval before checking again
        time.sleep(10)  # Adjust this interval as needed
except KeyboardInterrupt:
    # Handle Ctrl+C to gracefully exit the loop
    pass


    
if __name__== '__main__':
    app.run(debug=True)
