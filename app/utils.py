from flask import request, g
import uuid
from datetime import datetime
from typing import Dict, Optional
from app.models import CarPrediction
from app.database import SessionLocal

def get_client_ip():
    """Get client IP address considering proxy headers"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]

def save_prediction_to_db(car_data: Dict, predicted_price: float, user_ip: str = None, user_id: int = None) -> Optional[int]:
    """Save car prediction data to database"""
    if SessionLocal is None:
        return None
    
    session = SessionLocal()
    try:
        prediction = CarPrediction(
            year=car_data.get('year', 2020),
            brand=car_data.get('brand', 'unknown'),
            model=car_data.get('model', 'unknown'),
            color=car_data.get('color', 'unknown'),
            engine_config=car_data.get('engine_config', 'unknown'),
            horsepower=car_data.get('horsepower', 0),
            torque=car_data.get('torque', 0),
            weight_kg=car_data.get('weight_kg', 0),
            zero_to_60_s=car_data.get('zero_to_60_s', 0.0),
            top_speed_mph=car_data.get('top_speed_mph', 0),
            num_doors=car_data.get('num_doors', 2),
            transmission=car_data.get('transmission', 'unknown'),
            drivetrain=car_data.get('drivetrain', 'unknown'),
            market_region=car_data.get('market_region', 'unknown'),
            mileage=car_data.get('mileage', 0),
            num_owners=car_data.get('num_owners', 0),
            interior_material=car_data.get('interior_material', 'unknown'),
            brake_type=car_data.get('brake_type', 'unknown'),
            tire_brand=car_data.get('tire_brand', 'unknown'),
            last_service_date=car_data.get('last_service_date', ''),
            service_history=car_data.get('service_history', 'unknown'),
            warranty_years=car_data.get('warranty_years', 0),
            damage_cost=car_data.get('damage_cost', 0.0),
            damage_type=car_data.get('damage_type', 'none'),
            carbon_fiber_body=int(car_data.get('carbon_fiber_body', 0)),
            aero_package=int(car_data.get('aero_package', 0)),
            limited_edition=int(car_data.get('limited_edition', 0)),
            has_warranty=int(car_data.get('has_warranty', 0)),
            non_original_parts=int(car_data.get('non_original_parts', 0)),
            damage=int(car_data.get('damage', 0)),
            predicted_price=predicted_price,
            user_ip=user_ip,
            user_id=user_id,  # Link to user who made the prediction
            session_id=str(uuid.uuid4()),
            request_id=g.get('request_id', str(uuid.uuid4()))
        )
        session.add(prediction)
        session.commit()
        return prediction.id
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()