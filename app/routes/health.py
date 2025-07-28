from flask import Blueprint, jsonify, g
from datetime import datetime
from ..ml import model
from ..database import SessionLocal

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_status = 'connected' if SessionLocal else 'disconnected'
    model_status = 'loaded' if model else 'not loaded'
    
    return jsonify({
        'status': 'healthy',
        'environment': 'development',  # Should come from app config
        'model': model_status,
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat(),
        'request_id': g.get('request_id', 'unknown')
    })