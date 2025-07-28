from flask import Blueprint, request, jsonify, g, session
from sqlalchemy import func
from ..database import SessionLocal
from ..models import CarPrediction

history_bp = Blueprint('history', __name__)

@history_bp.route('/predictions/history', methods=['GET'])
def get_prediction_history():
    """Get recent predictions from database"""
    if SessionLocal is None:
        return jsonify({
            'error': 'Database not available',
            'request_id': g.get('request_id', 'unknown')
        }), 503
    
    try:
        limit = min(request.args.get('limit', 50, type=int), 500)
        offset = request.args.get('offset', 0, type=int)
        
        db_session = None
        db_session = SessionLocal()
        query = db_session.query(CarPrediction)
        
        # Filter by current user if authenticated
        user_id = session.get('user_id')
        if user_id:
            query = query.filter(CarPrediction.user_id == user_id)
        
        # Apply filters if provided
        if 'brand' in request.args:
            query = query.filter(CarPrediction.brand.ilike(f"%{request.args['brand']}%"))
        if 'model' in request.args:
            query = query.filter(CarPrediction.model.ilike(f"%{request.args['model']}%"))
        if 'year' in request.args:
            query = query.filter(CarPrediction.year == request.args['year'])
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        predictions = query.order_by(CarPrediction.created_at.desc())\
                         .offset(offset)\
                         .limit(limit)\
                         .all()
        
        result = {
            'success': True,
            'count': len(predictions),
            'total': total,
            'offset': offset,
            'limit': limit,
            'predictions': [pred.to_dict() for pred in predictions],
            'request_id': g.get('request_id', 'unknown')
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get prediction history',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 500
    finally:
        if db_session:
            db_session.close()