from flask import Blueprint, request, jsonify, g, session
import logging
from ..ml import model, predict_price
from ..utils import get_client_ip, save_prediction_to_db
from datetime import datetime

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict_car_price():
    """Main prediction endpoint"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'Service temporarily unavailable',
            'request_id': g.get('request_id', 'unknown')
        }), 503
    
    if not request.is_json:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Request must be JSON',
            'request_id': g.get('request_id', 'unknown')
        }), 400
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['brand', 'model', 'year']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Make prediction
        predicted_price = predict_price(data)
        
        # Save to database
        user_ip = get_client_ip()
        user_id = session.get('user_id')  # Get current user ID from session
        db_id = save_prediction_to_db(data, predicted_price, user_ip, user_id)
        
        response = {
            'success': True,
            'predicted_price': predicted_price,
            'currency': 'USD',
            'database_id': db_id,
            'input_data': data,
            'request_id': g.get('request_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat()
        }

        return jsonify(response)
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid data format',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 400
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 500