from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_coords = {'latitude': None, 'longitude': None}

# Enhanced HTML Page with embedded CSS and model info
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>AP360C – Accident Detection System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #dbeafe, #f0f9ff);
            color: #111827;
            text-align: center;
            padding: 40px;
        }
        .container {
            max-width: 700px;
            margin: auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1e3a8a;
        }
        .info {
            margin: 20px 0;
            font-size: 16px;
            color: #374151;
        }
        #status {
            margin-top: 20px;
            font-weight: bold;
            color: #0f5132;
        }
        #coords {
            margin-top: 10px;
            font-size: 15px;
            color: #1e40af;
        }
        .footer {
            margin-top: 40px;
            font-size: 13px;
            color: #6b7280;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚨 AP360C - AI-Powered Accident Detection</h1>
        <p class="info">
            This system detects road accidents in real time using a trained deep learning model.<br>
            Once an accident is detected, it triggers an emergency SMS and logs the location of the event.<br><br>
            Please allow location access to help us simulate the emergency detection.
        </p>

        <h2>📍 Fetching your location...</h2>
        <p id="status">Please wait...</p>
        <p id="coords"></p>

        <div class="footer">
            Developed with ❤️ by Team AP360C | Flask • OpenCV • Twilio • AI Model
        </div>
    </div>

    <script>
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            document.getElementById("coords").innerText = "Latitude: " + lat + ", Longitude: " + lon;

            fetch("/location", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    latitude: lat,
                    longitude: lon
                })
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      document.getElementById("status").innerText = "✅ Location sent successfully & emergency alert triggered.";
                  } else {
                      document.getElementById("status").innerText = "❌ Failed to send location.";
                  }
              });
        }, function(error) {
            document.getElementById("status").innerText = "⚠️ Failed to get location: " + error.message;
        });
    </script>
    <script>
  window.cbConfig = {
    chatId: "35838048-b088-4541-b6a8-e790a327495d"
  };
</script>
<script src="https://app.chatbit.co/embed.min.js" defer></script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/location', methods=['POST'])
def location():
    global latest_coords
    data = request.get_json()
    latest_coords['latitude'] = data['latitude']
    latest_coords['longitude'] = data['longitude']
    print(f"📍 Received location: {data}")
    return jsonify(success=True)

@app.route('/get_coords')
def get_coords():
    return jsonify(latest_coords)

if __name__ == '__main__':
    app.run(port=5000)
