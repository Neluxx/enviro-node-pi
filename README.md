# enviro-node-pi

A Python-Flask-based application for collecting environmental sensor data on a Raspberry Pi and sending it to a central hub for further analysis and processing.

## Features
- **Environmental Data Collection:**
    - Utilizes the **MH-Z19** sensor for CO₂ detection.
    - Reads temperature, humidity, and pressure from the **BME680** sensor.
    - Includes mock sensors for testing without physical hardware.

- **REST API:**
    - Exposes a Flask RESTful endpoint (`/sensor-data`) to retrieve sensor data.
    - Sends sensor data to a configured remote API via an HTTP POST request.

- **Error Handling:**
    - Handles HTTP and network-related errors during data transmission.
    - Provides meaningful error responses for easier debugging.

## Setup Instructions

### Prerequisites
- Hardware:
    - Raspberry Pi
    - **MH-Z19** and **BME680** sensors (optional for testing).
- Software:
    - Python 3.x
    - Required Python libraries (see [Dependencies](#dependencies)).

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/enviro-node-pi.git
   cd enviro-node-pi
   ```

2. Install dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and specify your central hub API URL:
   ```
   API_URL=http://your-central-hub-api-url
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

### Testing with Mock Sensors
The app includes mock data for testing when the required sensors are not physically connected. You can use the mock sensor classes to simulate various conditions.

## API Endpoints

### `/sensor-data`
- **Method:** `GET`
- **Description:** Retrieves environmental data from sensors and forwards it to the configured API endpoint.

#### Sample Response
- **Success:**
  ```json
  {
      "message": "Data sent successfully"
  }
  ```
- **Error:**
  ```json
  {
      "message": "Error sending POST request: [error details]"
  }
  ```

## Dependencies
- `Flask`: Python web framework.
- `requests`: For sending HTTP POST requests.
- Python libraries for sensors (**mh_z19**, **bme680**) when available.
- `python-dotenv`: For environment variable management.

Install dependencies:
```bash
pip install Flask flask-restful requests python-dotenv mh_z19 bme680
```

## Contributions
Contributions and suggestions are welcome! Please feel free to submit a pull request or open an issue for enhancements or bugs.

## License
This project is open-source and available under the [MIT License](LICENSE).
