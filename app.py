import os
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api
import requests
from dotenv import load_dotenv
from sensor import Sensor

CONTENT_TYPE_HEADER = {"Content-Type": "application/json"}

app = Flask(__name__)
api = Api(app)
load_dotenv()

class SensorData(Resource):
    def get(self):
        """Handle GET request to retrieve sensor data and send it to another API."""
        data = Sensor().get_data()
        return self.post_sensor_data(data)

    def post_sensor_data(self, data):
        """Send POST request with sensor data to another API."""
        api_url = os.getenv("API_URL")
        try:
            response = requests.post(api_url, json=data, headers=CONTENT_TYPE_HEADER)
            response.raise_for_status()
            return make_response(
                jsonify({"message": "Data sent successfully"}), response.status_code
            )
        except requests.exceptions.RequestException as req_err:
            return self.handle_request_exception(req_err, response)

    def handle_request_exception(self, error, response=None):
        """Handle exceptions during a POST request."""
        if isinstance(error, requests.exceptions.HTTPError) and response:
            return make_response(
                jsonify({"message": f"HTTP error occurred: {error}"}), response.status_code
            )
        return make_response(
            jsonify({"message": f"Error sending POST request: {error}"}), 500
        )

api.add_resource(SensorData, "/sensor-data")

if __name__ == "__main__":
    app.run(debug=True)
