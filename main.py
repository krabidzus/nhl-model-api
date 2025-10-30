from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# načti uložené váhy
with open("weights.json", "r") as f:
    weights = json.load(f)

@app.route("/")
def home():
    return jsonify({"status":"ok"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # očekáváme dict s home_stats a away_stats – uprav dle svého
    home = data.get("home_stats", {})
    away = data.get("away_stats", {})

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
        "predicted_winner": "home" if home_score>away_score else "away"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
