import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    JSON_SORT_KEYS = False
    MODEL_PATH = os.getenv('MODEL_PATH', 'supercar_price_prediction_model.pkl')
    DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        db=os.getenv('DB_NAME', 'car_predictions')
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL  
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
