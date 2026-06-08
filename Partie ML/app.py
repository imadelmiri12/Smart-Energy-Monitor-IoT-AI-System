from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)
CORS(app)

# ==========================================
# MONGODB
# ==========================================

client = MongoClient("mongodb://localhost:27017")

db = client["smart_energy_db"]

energy_collection = db["energy_data"]
anomaly_collection = db["energy_anomalies"]

# ==========================================
# API DASHBOARD
# ==========================================

@app.route("/api/dashboard")
def dashboard():

    data = list(
        energy_collection.find(
            {},
            {"_id": 0}
        )
    )

    if len(data) == 0:
        return jsonify({
            "error": "Aucune donnée disponible"
        })

    df = pd.DataFrame(data)

    total_mesures = len(df)

    consommation_moyenne = round(
        df["total"].mean(),
        2
    )

    lamp = round(df["lamp"].mean(), 2)
    tv = round(df["tv"].mean(), 2)
    fan = round(df["fan"].mean(), 2)
    pc = round(df["pc"].mean(), 2)
    ac = round(df["ac"].mean(), 2)
    wm = round(df["wm"].mean(), 2)

    devices = {
        "Lampe": lamp,
        "Télévision": tv,
        "Ventilateur": fan,
        "PC": pc,
        "Climatisation": ac,
        "Machine à laver": wm
    }

    ranking = sorted(
        devices.items(),
        key=lambda x: x[1],
        reverse=True
    )

    prix_kwh = 1.20

    cost_month = round(
        (consommation_moyenne / 1000)
        * 24
        * 30
        * prix_kwh,
        2
    )

    nb_anomalies = anomaly_collection.count_documents({})

    taux_anomalies = round(
        (nb_anomalies / total_mesures) * 100,
        2
    )

    return jsonify({

        "total_mesures": total_mesures,

        "nb_anomalies": nb_anomalies,

        "taux_anomalies": taux_anomalies,

        "consommation_moyenne": consommation_moyenne,

        "cout_mensuel": cost_month,

        "devices": {
            "lamp": lamp,
            "tv": tv,
            "fan": fan,
            "pc": pc,
            "ac": ac,
            "wm": wm
        },

        "ranking": ranking

    })


# ==========================================
# API HISTORY
# ==========================================

@app.route("/api/history")
def history():

    data = []

    for doc in energy_collection.find({}, {"_id": 0}):

        data.append({

            "timestamp": doc.get("timestamp"),
            "total": doc.get("total", 0),

            "lamp": doc.get("lamp", 0),
            "tv": doc.get("tv", 0),
            "fan": doc.get("fan", 0),
            "pc": doc.get("pc", 0),
            "ac": doc.get("ac", 0),
            "wm": doc.get("wm", 0)

        })

    return jsonify(data)


# ==========================================
# API ANOMALIES
# ==========================================

@app.route("/api/anomalies")
def anomalies():

    data = list(
        anomaly_collection.find(
            {},
            {"_id": 0}
        )
    )

    return jsonify(data)


# ==========================================
# TEST MONGODB
# ==========================================

@app.route("/api/test")
def test():

    count = energy_collection.count_documents({})

    return jsonify({
        "mongodb": "connecté",
        "documents": count
    })


# ==========================================
# LANCEMENT
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )