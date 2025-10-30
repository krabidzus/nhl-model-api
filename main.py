from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load saved weights
try:
    weights_path = os.path.join(os.path.dirname(__file__), "weights.json")
    with open(weights_path, "r") as f:
        weights = json.load(f)
    print(f"Loaded weights: {weights}")
except Exception as e:
    print(f"Error loading weights: {e}")
    weights = {}

@app.route("/")
def home():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get home and away stats
        home = data.get("home_stats", {})
        away = data.get("away_stats", {})
        
        if not home or not away:
            return jsonify({"error": "Missing home_stats or away_stats"}), 400
        
        def score(stats):
            s = 0.0
            for k, w in weights.items():
                s += stats.get(k, 0) * w
            return s
        
        home_score = score(home)
        away_score = score(away)
        
        return jsonify({
            "home_score": home_score,
            "away_score": away_score,
            "predicted_winner": "home" if home_score > away_score else "away"
        })
    
    except Exception as e:
        print(f"Error in predict endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)