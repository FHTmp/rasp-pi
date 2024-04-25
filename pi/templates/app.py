from flask import Flask, render_template, jsonify
#from sense_emu import SenseHat
from setuptools import setup

sense= setup()


#sense = SenseHat()


app = Flask (__name__)

@app.route('/')
def index():
    temperature, humidity = get_temperature_and_humidity()
    warning_message = 'Warning High Temperature or humidity!'
    return render_template('index.html', temperature=temperature, humidity=humidity, warning=warning_message)



def get_temperature_and_humidity():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    return temperature, humidity




if __name__== '__main__':
    app.run(debug=True)
