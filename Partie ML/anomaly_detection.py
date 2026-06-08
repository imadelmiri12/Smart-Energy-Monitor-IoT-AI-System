from pymongo import MongoClient
import pandas as pd
from sklearn.ensemble import IsolationForest

# =====================================================
# CONNEXION MONGODB
# =====================================================

try:
    client = MongoClient("mongodb://localhost:27017")
    db = client["smart_energy_db"]

    energy_collection = db["energy_data"]
    anomaly_collection = db["energy_anomalies"]

    print("Connexion MongoDB réussie")

except Exception as e:
    print("Erreur MongoDB :", e)
    exit()

# =====================================================
# CHARGEMENT DES DONNEES
# =====================================================

data = list(energy_collection.find())

if len(data) < 20:
    print("Pas assez de données pour lancer l'analyse IA.")
    exit()

df = pd.DataFrame(data)

features = [
    "lamp",
    "tv",
    "fan",
    "pc",
    "ac",
    "wm",
    "total"
]

# Vérification des colonnes

for col in features:
    if col not in df.columns:
        print(f"Colonne manquante : {col}")
        exit()

# Conversion timestamp

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

# =====================================================
# DETECTION D'ANOMALIES
# =====================================================

X = df[features]

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)

df["anomaly"] = model.predict(X)

df["anomaly"] = df["anomaly"].map({
    1: "Normal",
    -1: "Anomalie"
})

# =====================================================
# APPAREILS
# =====================================================

devices_names = {
    "lamp": "Lampe",
    "tv": "Télévision",
    "fan": "Ventilateur",
    "pc": "Ordinateur",
    "ac": "Climatisation",
    "wm": "Machine à laver"
}

# =====================================================
# RAPPORT DES ANOMALIES
# =====================================================

print("\n")
print("=" * 60)
print("RAPPORT D'ANALYSE ENERGETIQUE")
print("=" * 60)

anomalies = df[df["anomaly"] == "Anomalie"]

if len(anomalies) == 0:

    print("\nAucune anomalie détectée.\n")

else:

    print(f"\nNombre d'anomalies détectées : {len(anomalies)}\n")

    for _, row in anomalies.iterrows():

        consommation = {
            "lamp": row["lamp"],
            "tv": row["tv"],
            "fan": row["fan"],
            "pc": row["pc"],
            "ac": row["ac"],
            "wm": row["wm"]
        }

        appareil = max(
            consommation,
            key=consommation.get
        )

        puissance = consommation[appareil]

        # Conseils intelligents

        if appareil == "ac":

            conseil = (
                "Réduire l'utilisation de la climatisation "
                "ou augmenter légèrement la température cible."
            )

        elif appareil == "wm":

            conseil = (
                "Reporter le fonctionnement de la machine "
                "à laver en dehors des heures de pointe."
            )

        elif appareil == "pc":

            conseil = (
                "Vérifier les applications gourmandes "
                "en énergie sur le PC."
            )

        elif appareil == "tv":

            conseil = (
                "Éteindre la télévision lorsqu'elle "
                "n'est pas utilisée."
            )

        elif appareil == "fan":

            conseil = (
                "Vérifier si le ventilateur fonctionne "
                "inutilement."
            )

        else:

            conseil = (
                "Contrôler les appareils électriques "
                "actuellement actifs."
            )

        print("-" * 60)

        if "timestamp" in df.columns:
            print("Date :", row["timestamp"])

        print("Consommation totale :", row["total"], "W")
        print("Etat :", row["anomaly"])
        print("Appareil dominant :", devices_names[appareil])
        print("Puissance :", puissance, "W")
        print("Conseil :", conseil)

        # Sauvegarde anomalie

        anomaly_collection.insert_one({
            "timestamp": str(row.get("timestamp", "")),
            "total": float(row["total"]),
            "device": devices_names[appareil],
            "power": float(puissance),
            "advice": conseil
        })

# =====================================================
# CLASSEMENT DES APPAREILS
# =====================================================

print("\n")
print("=" * 60)
print("CLASSEMENT DES APPAREILS")
print("=" * 60)

devices_mean = {
    "Lampe": df["lamp"].mean(),
    "Télévision": df["tv"].mean(),
    "Ventilateur": df["fan"].mean(),
    "Ordinateur": df["pc"].mean(),
    "Climatisation": df["ac"].mean(),
    "Machine à laver": df["wm"].mean()
}

ranking = sorted(
    devices_mean.items(),
    key=lambda x: x[1],
    reverse=True
)

total_mean = sum(devices_mean.values())

for i, (device, power) in enumerate(ranking, start=1):

    percentage = round(
        (power / total_mean) * 100,
        2
    )

    print(
        f"{i}. {device:<20}"
        f"{power:.2f} W "
        f"({percentage} %)"
    )

# =====================================================
# ESTIMATION DES COUTS
# =====================================================

print("\n")
print("=" * 60)
print("ESTIMATION DES COUTS")
print("=" * 60)

prix_kwh = 1.20

mean_power = df["total"].mean()

kwh = mean_power / 1000

cost_hour = kwh * prix_kwh
cost_day = cost_hour * 24
cost_month = cost_day * 30

print(f"Consommation moyenne : {mean_power:.2f} W")
print(f"Coût horaire estimé : {cost_hour:.2f} MAD")
print(f"Coût journalier estimé : {cost_day:.2f} MAD")
print(f"Coût mensuel estimé : {cost_month:.2f} MAD")

# =====================================================
# STATISTIQUES GLOBALES
# =====================================================

print("\n")
print("=" * 60)
print("STATISTIQUES")
print("=" * 60)

nb_mesures = len(df)
nb_anomalies = len(anomalies)

taux = round(
    (nb_anomalies / nb_mesures) * 100,
    2
)

print("Nombre total de mesures :", nb_mesures)
print("Nombre d'anomalies :", nb_anomalies)
print("Taux d'anomalies :", taux, "%")

print("\nAnalyse terminée avec succès.")