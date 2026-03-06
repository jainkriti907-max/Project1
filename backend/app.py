import os
import logging
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from trend_engine import run_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Mosaic Trends Radar API"}), 200

@app.route('/scan', methods=['POST', 'OPTIONS'])
def scan():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response, 200
    try:
        body = request.get_json(silent=True) or {}
        logger.info(f"Scan requested: {body}")
        trends = run_pipeline()
        return jsonify({
            "success": True,
            "scan_id": f"scan_{int(time.time())}",
            "count": len(trends),
            "trends": trends,
        }), 200
    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
