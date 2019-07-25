
import json
import random
import time
from datetime import datetime
from heartbeat import heartrate

from flask import Flask, Response, render_template

application = Flask(__name__)
random.seed()  # Initialize the random number generator


@application.route('/')
def index():
    return render_template('chart.html')


@application.route('/chart-data')
def chart_data():
    start_time = time.time()
    def get_sensor_data():
        while True:
            print("Waiting for heartrate")
            number = heartrate()
            timing = round(time.time() - start_time, 0)
            json_data = json.dumps(
                {'time': str(timing) + 'sec' , 'value': number}) 
            print("Got heartrate")

            yield f"data:{json_data}\n\n"
            time.sleep(1)

            
            
    def generate_random_data():
        timing = 0
        while True:
            number = random.randint(56, 79)
            timing += 5
            json_data = json.dumps(
                {'time': str(timing) + 'sec' , 'value': number}) 
            yield f"data:{json_data}\n\n"
            time.sleep(5)

    return Response(get_sensor_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
