from flask import Blueprint, jsonify, g, session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..database import SessionLocal
from ..models import CarPrediction

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/predictions/stats', methods=['GET'])
def get_prediction_stats():
    """Get aggregated prediction statistics"""
    if SessionLocal is None:
        return jsonify({
            'error': 'Database not available',
            'request_id': g.get('request_id', 'unknown')
        }), 503
    
    try:
        db_session = None
        db_session = SessionLocal()
        
        # Filter by current user if authenticated
        user_id = session.get('user_id')
        base_query = db_session.query(CarPrediction)
        if user_id:
            base_query = base_query.filter(CarPrediction.user_id == user_id)
        
        # Basic stats
        stats = base_query.with_entities(
            func.count(CarPrediction.id).label('total_predictions'),
            func.avg(CarPrediction.predicted_price).label('avg_price'),
            func.max(CarPrediction.predicted_price).label('max_price'),
            func.min(CarPrediction.predicted_price).label('min_price'),
            func.stddev(CarPrediction.predicted_price).label('price_stddev')
        ).first()
        
        # Popular brands
        popular_brands = base_query.with_entities(
            CarPrediction.brand,
            func.count(CarPrediction.id).label('count')
        ).group_by(CarPrediction.brand)\
         .order_by(func.count(CarPrediction.id).desc())\
         .limit(5)\
         .all()
        
        # Recent activity
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_count = base_query.filter(CarPrediction.created_at >= yesterday).count()
        
        result = {
            'total_predictions': stats.total_predictions or 0,
            'average_price': float(stats.avg_price or 0),
            'maximum_price': float(stats.max_price or 0),
            'minimum_price': float(stats.min_price or 0),
            'price_standard_deviation': float(stats.price_stddev or 0),
            'popular_brands': [{'brand': b.brand, 'count': b.count} for b in popular_brands],
            'recent_predictions_24h': recent_count,
            'request_id': g.get('request_id', 'unknown')
        }
        
        return jsonify({
            'success': True,
            'stats': result
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get prediction stats',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 500
    finally:
        if db_session:
            db_session.close()