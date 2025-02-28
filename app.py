from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import joblib
from pymodbus.client import ModbusSerialClient

app = Flask(__name__)

# Load Models and Scalers
anomaly_model = joblib.load("isolation_forest_model.pkl")
predictive_model = joblib.load("predictive_maintenance_model.pkl")
predictive_scaler = joblib.load("scaler2.pkl")
predictive_features = joblib.load("selected_features.pkl")
oee_model = joblib.load("oee_model_tuned.pkl")
oee_scaler = joblib.load("scaler3.pkl")
oee_features = joblib.load("selected_features.pkl")  # Separate feature set for OEE

# Modbus Configuration
client = ModbusSerialClient(port="COM7", baudrate=19200, stopbits=1, bytesize=8, parity="N", timeout=3)

REGISTER_MAPPING = {
    "Z-Axis RMS Velocity (in/sec)": 45201 - 40001,
    "Temperature (°F)": 45203 - 40001,
    "Z-Axis Peak Acceleration (G)": 45207 - 40001,
    "X-Axis Peak Acceleration (G)": 45208 - 40001,
    "Z-Axis Peak Velocity (mm/sec)": 45218 - 40001,
    "X-Axis RMS Velocity (in/sec)": 45205 - 40001,
}
SCALING_FACTORS = {
    "Z-Axis RMS Velocity (in/sec)": 6.5535 / 65535,
    "Temperature (°F)": 327.67 / 32767,
    "Z-Axis Peak Acceleration (G)": 65.535 / 65535,
    "X-Axis Peak Acceleration (G)": 65.535 / 65535,
    "Z-Axis Peak Velocity (mm/sec)": 65.535 / 65535,
    "X-Axis RMS Velocity (in/sec)": 6.5535 / 65535,
}
def read_modbus_data():
    """ Reads sensor data from Modbus and returns a dictionary of feature values. """
    if not client.connect():
        return {"error": "Failed to connect to Modbus device"}
    
    data = {}
    for feature, address in REGISTER_MAPPING.items():
        try:
            response = client.read_holding_registers(address=address, count=1, slave=1)
            if response and response.registers:
                data[feature] = round(response.registers[0] * SCALING_FACTORS[feature], 3)
            else:
                data[feature] = 0  # ✅ Set default value if no data
        except Exception as e:
            data[feature] = 0  # ✅ Set default value in case of error

    return data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect_anomaly', methods=['GET'])
def detect_anomaly():
    live_data = read_modbus_data()
    if not live_data:
        return jsonify({"error": "Failed to read sensor data"}), 500
    
    df = pd.DataFrame([live_data])
    
    # Convert DataFrame to NumPy array to remove feature names
    prediction = anomaly_model.predict(df.to_numpy())  
    
    return jsonify({"status": "Anomaly" if prediction[0] == -1 else "Normal", "data": live_data})


@app.route('/predict_maintenance', methods=['GET'])
def predict_maintenance():
    """ Predicts maintenance needs using predictive maintenance model. """
    live_data = read_modbus_data()
    if "error" in live_data:
        return jsonify({"error": live_data["error"]}), 500
    
    df = pd.DataFrame([live_data])

    # ✅ Ensure only required features are used
    missing_features = [feat for feat in predictive_features if feat not in df.columns]
    if missing_features:
        return jsonify({"error": f"Missing features for predictive maintenance: {missing_features}"}), 500
    
    df = df[predictive_features]  # Select required features
    df_scaled = pd.DataFrame(predictive_scaler.transform(df), columns=predictive_features)  
    prediction = predictive_model.predict(df_scaled)[0]
    
    return jsonify({"status": "Failure Detected" if prediction == 1 else "No Issue", "data": live_data})

@app.route('/calculate_oee', methods=['GET'])
def calculate_oee():
    """ Calculates OEE using the trained model without using selected_features.pkl. """
    live_data = read_modbus_data()
    if "error" in live_data:
        return jsonify({"error": live_data["error"]}), 500

    df = pd.DataFrame([live_data])

    # ✅ Define required OEE model features manually (based on training)
    required_features = [
        "Z-Axis RMS Velocity (in/sec)",
        "Temperature (°F)",
        "Z-Axis Peak Acceleration (G)",
        "X-Axis Peak Acceleration (G)",
        "Z-Axis Peak Velocity (mm/sec)",
        "X-Axis RMS Velocity (in/sec)",
    ]

    # ✅ Remove extra features and fill missing ones with 0
    df = df.reindex(columns=required_features, fill_value=0)

    # ✅ Scale the data before prediction
    df_scaled = pd.DataFrame(oee_scaler.transform(df), columns=required_features)  
    oee_prediction = oee_model.predict(df_scaled)[0]

    return jsonify({"OEE": round(oee_prediction, 3), "data": live_data})

if __name__ == '__main__':
    app.run(debug=True)
