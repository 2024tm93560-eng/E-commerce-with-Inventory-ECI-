Set-Content -Path "D:\common-repo\services\Eci-dashboard\app.py" -Encoding UTF8 -Value @'
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/")
def index():
    return "ECI Dashboard is up", 200
'@
