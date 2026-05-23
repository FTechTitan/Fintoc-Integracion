import os
import hmac
import hashlib
import json
import requests
from flask import Flask, request, jsonify, render_template, redirect
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

app = Flask(__name__)

FINTOC_SECRET_KEY = os.getenv("FINTOC_SECRET_KEY")
FINTOC_PUBLIC_KEY = os.getenv("FINTOC_PUBLIC_KEY")
WEBHOOK_SECRET    = os.getenv("FINTOC_WEBHOOK_SECRET", "whsec_test_sDQqWhPbd4StPXgeQ33qwnEv")
FINTOC_API        = "https://api.fintoc.com/v1"

# Split: % que retiene TrypoPMS
TRYPO_COMISION_PCT = 0.20  # 20%
BASE_URL = os.getenv("BASE_URL", "https://example.com")  # debe ser HTTPS

if not FINTOC_SECRET_KEY:
    raise RuntimeError("FINTOC_SECRET_KEY no definida en .env")


def _headers():
    return {"Authorization": f"Bearer {FINTOC_SECRET_KEY}"}


def fintoc_post(path, payload):
    r = requests.post(
        f"{FINTOC_API}{path}",
        json=payload,
        headers=_headers(),
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def fintoc_get(path):
    r = requests.get(
        f"{FINTOC_API}{path}",
        headers=_headers(),
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def calcular_split(monto_total):
    trypo = round(monto_total * TRYPO_COMISION_PCT)
    alojamiento = monto_total - trypo
    return {"trypo": trypo, "alojamiento": alojamiento, "total": monto_total}


@app.route("/")
def index():
    return render_template("index.html", public_key=FINTOC_PUBLIC_KEY)


@app.route("/crear-pago", methods=["POST"])
def crear_pago():
    data = request.json or {}
    monto    = int(data.get("monto", 50000))
    email    = data.get("email", "")
    reserva  = data.get("reserva_id", "DEMO-001")
    nombre   = data.get("nombre_alojamiento", "Alojamiento Demo")

    session = fintoc_post("/checkout_sessions", {
        "amount": monto,
        "currency": "CLP",
        "success_url": f"{BASE_URL}/success?reserva={reserva}",
        "cancel_url":  f"{BASE_URL}/cancel",
        "customer_email": email or None,
        "business_profile": {"name": nombre},
        "metadata": {
            "reserva_id": reserva,
            "split": json.dumps(calcular_split(monto)),
        },
    })

    return jsonify({
        "checkout_url": session["redirect_url"],
        "session_id": session["id"],
        "split": calcular_split(monto),
    })


@app.route("/success")
def success():
    reserva = request.args.get("reserva", "")
    return render_template("success.html", reserva=reserva)


@app.route("/cancel")
def cancel():
    return render_template("cancel.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    payload   = request.get_data()
    sig_header = request.headers.get("Fintoc-Signature", "")

    # Validar firma
    secret = WEBHOOK_SECRET.encode()
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig_header):
        app.logger.warning("Webhook firma inválida")
        return jsonify({"error": "firma inválida"}), 400

    event = json.loads(payload)
    app.logger.info(f"Evento recibido: {event['type']}")

    if event["type"] == "payment_intent.succeeded":
        pi      = event["data"]
        monto   = pi["amount"]
        split   = calcular_split(monto)
        pi_id   = pi["id"]
        reserva = pi.get("metadata", {}).get("reserva_id", "?")

        app.logger.info(
            f"[SPLIT] Reserva {reserva} | PI {pi_id} | "
            f"Total: ${monto:,} CLP | "
            f"TrypoPMS: ${split['trypo']:,} | "
            f"Alojamiento: ${split['alojamiento']:,}"
        )
        # Aquí iría fintoc_post("/v2/transfers", {...}) cuando el balance sea > 0

    return jsonify({"received": True}), 200


if __name__ == "__main__":
    app.run(debug=False, port=5000, use_reloader=False)
