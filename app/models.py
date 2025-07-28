from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from typing import Dict
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class CarPrediction(Base):
    __tablename__ = 'car_predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    color = Column(String(50), nullable=False)
    engine_config = Column(String(50), nullable=False)
    horsepower = Column(Integer, nullable=False)
    torque = Column(Integer, nullable=False)
    weight_kg = Column(Integer, nullable=False)
    zero_to_60_s = Column(Float, nullable=False)
    top_speed_mph = Column(Integer, nullable=False)
    num_doors = Column(Integer, nullable=False)
    transmission = Column(String(50), nullable=False)
    drivetrain = Column(String(50), nullable=False)
    market_region = Column(String(100), nullable=False)
    mileage = Column(Integer, nullable=False)
    num_owners = Column(Integer, nullable=False)
    interior_material = Column(String(50), nullable=False)
    brake_type = Column(String(50), nullable=False)
    tire_brand = Column(String(50), nullable=False)
    last_service_date = Column(String(20), nullable=True)
    service_history = Column(String(50), nullable=False)
    warranty_years = Column(Integer, nullable=False)
    damage_cost = Column(Float, nullable=False, default=0.0)
    damage_type = Column(String(50), nullable=True)
    carbon_fiber_body = Column(Integer, nullable=False, default=0)
    aero_package = Column(Integer, nullable=False, default=0)
    limited_edition = Column(Integer, nullable=False, default=0)
    has_warranty = Column(Integer, nullable=False, default=0)
    non_original_parts = Column(Integer, nullable=False, default=0)
    damage = Column(Integer, nullable=False, default=0)
    predicted_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_ip = Column(String(45), nullable=True)
    session_id = Column(String(100), nullable=True)
    request_id = Column(String(100), nullable=True)
    user_id = Column(Integer, nullable=True)  # Link to user who made the prediction

    def to_dict(self) -> Dict:
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'year': self.year,
            'brand': self.brand,
            'model': self.model,
            'color': self.color,
            'engine_config': self.engine_config,
            'horsepower': self.horsepower,
            'torque': self.torque,
            'weight_kg': self.weight_kg,
            'zero_to_60_s': self.zero_to_60_s,
            'top_speed_mph': self.top_speed_mph,
            'num_doors': self.num_doors,
            'transmission': self.transmission,
            'drivetrain': self.drivetrain,
            'market_region': self.market_region,
            'mileage': self.mileage,
            'num_owners': self.num_owners,
            'interior_material': self.interior_material,
            'brake_type': self.brake_type,
            'tire_brand': self.tire_brand,
            'last_service_date': self.last_service_date,
            'service_history': self.service_history,
            'warranty_years': self.warranty_years,
            'damage_cost': self.damage_cost,
            'damage_type': self.damage_type,
            'carbon_fiber_body': bool(self.carbon_fiber_body),
            'aero_package': bool(self.aero_package),
            'limited_edition': bool(self.limited_edition),
            'has_warranty': bool(self.has_warranty),
            'non_original_parts': bool(self.non_original_parts),
            'damage': bool(self.damage),
            'predicted_price': self.predicted_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_ip': self.user_ip,
            'session_id': self.session_id,
            'request_id': self.request_id,
            'user_id': self.user_id
        }
