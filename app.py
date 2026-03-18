import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')


# -----------------------------
# CONTACT (Exercice 6)
# -----------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# -----------------------------
# API PARIS (Exercice 2)
# -----------------------------
@app.get("/paris")
def api_paris():

    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)


# -----------------------------
# RAPPORT (Exercice 3/4)
# -----------------------------
@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")


# -----------------------------
# HISTOGRAMME (Exercice 5)
# -----------------------------
@app.get("/temperatures/daily")
def api_paris_daily():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=48.8566&longitude=2.3522"
        "&daily=temperature_2m_max"
        "&timezone=Europe%2FParis"
    )

    r = requests.get(url)
    data = r.json()

    days = data.get("daily", {}).get("time", [])
    tmax = data.get("daily", {}).get("temperature_2m_max", [])

    n = min(len(days), len(tmax))
    result = [{"date": days[i], "tmax": tmax[i]} for i in range(n)]

    return jsonify(result)


@app.route("/histogramme")
def histogramme():
    return render_template("histogramme.html")


# -----------------------------
# ATELIER (Gauge Humidité Versailles)
# -----------------------------
@app.get("/versailles/humidity")
def api_versailles_humidity():

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=48.8014&longitude=2.1301"
        "&current=relative_humidity_2m"
        "&timezone=Europe%2FParis"
    )

    r = requests.get(url)
    data = r.json()

    current = data.get("current", {})

    return jsonify({
        "datetime": current.get("time"),
        "humidity": current.get("relative_humidity_2m")
    })


@app.route("/atelier")
def atelier():
    return render_template("atelier.html")


# -----------------------------
# LANCEMENT SERVEUR
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
