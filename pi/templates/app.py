from flask import Flask, jsonify, render_template
from sense_emu import SenseHat
import time

app = Flask(__name__)
sense = SenseHat()

# Define the temperature and humidity thresholds
TEMP_THRESHOLD = 40  # Threshold temperature in Celsius
HUMIDITY_THRESHOLD = 90  # Threshold humidity in percentage

@app.route('/')
def index():
    try:
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        warning = check_and_display_warning(temperature, humidity)
        data = {
            'temperature': temperature,
            'humidity': humidity,
            'warning': warning
        }
        return jsonify(data)
    except Exception as e:
        # Log the error for debugging purposes
        print("An error occurred:", e)
        return jsonify({'error': str(e)}), 500

def check_and_display_warning(temperature, humidity):
    # Check if temperature or humidity exceeds thresholds
    if temperature > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
        # Construct the warning message
        warning_message = "WARNING: "

        if temperature > TEMP_THRESHOLD:
            warning_message += f"Temperature ({temperature:.2f}°C) exceeds {TEMP_THRESHOLD}°C. "
        if humidity > HUMIDITY_THRESHOLD:
            warning_message += f"Humidity ({humidity:.2f}%) exceeds {HUMIDITY_THRESHOLD}%. "
        
        # Display warning message on the Sense emulator
        sense.show_message(warning_message, text_colour=[255, 0, 0])  # Red text

        return warning_message
    else:
        # No warning, clear any existing messages on the Sense emulator
        sense.clear()
        return None

import warnings

# Suppress specific warning from sense_hat library
warnings.filterwarnings("ignore", message="No emulator detected", category=UserWarning)

if __name__ == '__main__':    
    app.run(debug=True)

