"""
Mosaic Trends Radar — Flask Backend API
Exposes POST /scan endpoint for the frontend dashboard.
"""
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from trend_engine import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s — %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Allow CORS from Vercel frontend and localhost
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.vercel.app",
            os.getenv("FRONTEND_URL", "*"),
        ]
    }
})


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Mosaic Trends Radar API",
        "version": "1.0.0",
    }), 200


@app.route('/scan', methods=['POST', 'OPTIONS'])
def scan():
    """
    Run the Mosaic Trends Radar analysis pipeline.
    
    Request body (optional):
    {
        "category": "wellness",  // default
        "region": "IN"           // default
    }
    
    Response:
    {
        "trends": [...],
        "count": int,
        "scan_id": str
    }
    """
    if request.method == 'OPTIONS':
        return _cors_preflight()
    
    try:
        body = request.get_json(silent=True) or {}
        category = body.get('category', 'wellness')
        region = body.get('region', 'IN')
        
        logger.info(f"🔍 Scan requested — category={category}, region={region}")
        
        trends = run_pipeline()
        
        import time
        scan_id = f"scan_{int(time.time())}"
        
        return jsonify({
            "success": True,
            "scan_id": scan_id,
            "count": len(trends),
            "trends": trends,
            "meta": {
                "category": category,
                "region": region,
                "sources": ["Google Trends", "Reddit", "PubMed"],
                "model_version": "1.0.0",
            }
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Scan failed: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Trend scan failed. Please try again.",
        }), 500


def _cors_preflight():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response, 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    logger.info(f"🌿 Mosaic Trends Radar API starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
