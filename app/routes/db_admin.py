from flask import Blueprint, jsonify, g
from ..database import init_db, SessionLocal

db_admin_bp = Blueprint('db_admin', __name__)

@db_admin_bp.route('/database/init', methods=['POST'])
def initialize_database():
    """Initialize/recreate database tables"""
    try:
        success = init_db()
        if success:
            return jsonify({
                'success': True,
                'message': 'Database initialized successfully',
                'request_id': g.get('request_id', 'unknown')
            })
        return jsonify({
            'success': False,
            'message': 'Database initialization failed',
            'request_id': g.get('request_id', 'unknown')
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Database initialization error',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 500