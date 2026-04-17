from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# -------------------- HOME --------------------
@app.route('/')
def home():
    return "Precision Irrigation System Running ✅"

# -------------------- UI PAGE --------------------
@app.route('/ui')
def ui():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Precision Irrigation System</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                background: #f4f7f6;
                margin-top: 50px;
            }
            h2 {
                color: #2c7a7b;
            }
            input {
                padding: 10px;
                margin: 10px;
                width: 200px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                padding: 10px 20px;
                background: #2c7a7b;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #225e5f;
            }
            #result {
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <h2>🌱 Precision Irrigation System</h2>

        <input id="moisture" placeholder="Soil Moisture (%)"><br>
        <input id="temperature" placeholder="Temperature (°C)"><br>
        <input id="humidity" placeholder="Humidity (%)"><br>

        <button onclick="predict()">Check Irrigation</button>

        <div id="result"></div>

        <script>
            function predict() {
                let moisture = document.getElementById("moisture").value;
                let temp = document.getElementById("temperature").value;
                let humidity = document.getElementById("humidity").value;

                fetch("/predict", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        soil_moisture: parseInt(moisture) || 0,
                        temperature: parseInt(temp) || 0,
                        humidity: parseInt(humidity) || 0
                    })
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById("result").innerHTML =
                        "💧 Irrigation: <b>" + data.irrigation + "</b><br>" +
                        "📢 " + data.recommendation + "<br><br>" +
                        "🌡 Temp: " + data.temperature + "°C | 💦 Humidity: " + data.humidity + "%";
                })
                .catch(err => {
                    document.getElementById("result").innerText = "Error connecting to server";
                });
            }
        </script>

    </body>
    </html>
    """)

# -------------------- PREDICT API --------------------
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    soil_moisture = data.get("soil_moisture", 0)
    temperature = data.get("temperature", random.randint(20, 40))
    humidity = data.get("humidity", random.randint(30, 80))

    # ML logic
    if soil_moisture < 30:
        irrigation = "ON"
        recommendation = "Soil is dry. Activate irrigation."
    elif soil_moisture < 50:
        irrigation = "ON"
        recommendation = "Moderate moisture. Light irrigation recommended."
    else:
        irrigation = "OFF"
        recommendation = "Soil moisture sufficient. No irrigation needed."

    return jsonify({
        "irrigation": irrigation,
        "recommendation": recommendation,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# -------------------- STATUS --------------------
@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "service": "Precision Irrigation System"
    })

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)