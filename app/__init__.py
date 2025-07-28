from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
import logging
import os

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Set secret key for sessions
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # Configure session settings for proper cookie handling
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS attacks
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours in seconds
    app.config['SESSION_COOKIE_NAME'] = 'supercar_session'
    
    # Middleware
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    
    # Configure CORS to support credentials and cross-origin requests
    CORS(app, 
         supports_credentials=True,
         origins=['http://localhost:5000', 'http://127.0.0.1:5000'],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    
    # Initialize extensions
    from .database import init_db
    from .ml import init_ml
    
    # Initialize database and ML model
    init_db(app)
    init_ml(app)
    
    # Register blueprints
    from .routes.health import health_bp
    from .routes.predict import predict_bp
    from .routes.history import history_bp
    from .routes.stats import stats_bp
    from .routes.db_admin import db_admin_bp
    from .routes.auth import auth_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(db_admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register middleware
    register_middleware(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        from flask import jsonify, g
        app.logger.warning(f"Bad request: {str(error)}")
        return jsonify({
            'error': 'Bad request',
            'message': str(error),
            'request_id': g.get('request_id', 'unknown')
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        from flask import jsonify, g, request
        app.logger.warning(f"Not found: {request.path}")
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found',
            'request_id': g.get('request_id', 'unknown')
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify, g
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred',
            'request_id': g.get('request_id', 'unknown')
        }), 500

def register_middleware(app):
    """Register middleware for the application"""
    from flask import g, request
    from datetime import datetime
    import uuid
    
    @app.before_request
    def before_request():
        """Process before each request"""
        g.start_time = datetime.now()
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        
        if request.endpoint != 'health.health_check':
            app.logger.info(f"Incoming request {request.method} {request.path} - ID: {g.request_id}")

    @app.after_request
    def after_request(response):
        """Process after each request"""
        if request.endpoint != 'health.health_check':
            duration = (datetime.now() - g.start_time).total_seconds() * 1000
            app.logger.info(
                f"Completed {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.2f}ms - "
                f"ID: {g.request_id}"
            )
            response.headers['X-Request-ID'] = g.request_id
            response.headers['X-Request-Duration'] = f"{duration:.2f}ms"
        
        return response