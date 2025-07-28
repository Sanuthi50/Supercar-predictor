import joblib
import numpy as np
import pandas as pd
import logging

model = None

def init_ml(app):
    """Load the trained model from file"""
    global model
    try:
        model = joblib.load(app.config['MODEL_PATH'])
        app.logger.info(f"Model loaded successfully from {app.config['MODEL_PATH']}")
        
        # Validate model has required methods
        if not (hasattr(model, 'predict') and callable(model.predict)):
            raise AttributeError("Loaded model does not have predict method")
            
        return True
    except Exception as e:
        app.logger.error(f"Error loading model: {str(e)}")
        model = None
        return False

def create_prediction_dataframe(data):
    """Create a pandas DataFrame with the exact structure expected by the model"""
    expected_columns = [
        'year', 'brand', 'color', 'carbon_fiber_body', 'engine_config',
        'horsepower', 'torque', 'weight_kg', 'zero_to_60_s', 'top_speed_mph',
        'num_doors', 'transmission', 'drivetrain', 'market_region', 'mileage',
        'num_owners', 'interior_material', 'brake_type', 'tire_brand',
        'aero_package', 'limited_edition', 'has_warranty', 'last_service_date',
        'service_history', 'non_original_parts', 'model', 'warranty_years',
        'damage', 'damage_cost', 'damage_type'
    ]
    
    # Create dictionary with default values
    df_data = {col: [data.get(col)] if col in data else [None] for col in expected_columns}
    
    # Set default values for missing columns
    defaults = {
        'carbon_fiber_body': 0,
        'aero_package': 0,
        'limited_edition': 0,
        'has_warranty': 0,
        'non_original_parts': 0,
        'damage': 0,
        'year': 2020,
        'horsepower': 0,
        'torque': 0,
        'weight_kg': 0,
        'top_speed_mph': 0,
        'num_doors': 2,
        'mileage': 0,
        'num_owners': 0,
        'warranty_years': 0,
        'zero_to_60_s': 0.0,
        'damage_cost': 0.0,
        'brand': 'unknown',
        'color': 'unknown',
        'engine_config': 'unknown',
        'transmission': 'unknown',
        'drivetrain': 'unknown',
        'market_region': 'unknown',
        'interior_material': 'unknown',
        'brake_type': 'unknown',
        'tire_brand': 'unknown',
        'last_service_date': '',
        'service_history': 'unknown',
        'model': 'unknown',
        'damage_type': 'none'
    }
    
    for col, default in defaults.items():
        if df_data[col][0] is None:
            df_data[col][0] = default
    
    # Create DataFrame
    df = pd.DataFrame(df_data)
    
    # Convert data types
    int_cols = ['year', 'carbon_fiber_body', 'horsepower', 'torque', 'weight_kg',
               'top_speed_mph', 'num_doors', 'mileage', 'num_owners',
               'aero_package', 'limited_edition', 'has_warranty',
               'non_original_parts', 'warranty_years', 'damage']
    float_cols = ['zero_to_60_s', 'damage_cost']
    
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
    
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype('float64')
    
    return df

def predict_price(data):
    """Make a prediction using the loaded model"""
    if model is None:
        raise RuntimeError("Model not loaded")
    
    df = create_prediction_dataframe(data)
    prediction = model.predict(df)
    return float(prediction[0] if isinstance(prediction, np.ndarray) else float(prediction))