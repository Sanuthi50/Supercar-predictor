from .predict import predict_bp
from .health import health_bp
from .stats import stats_bp
from .history import history_bp
from .db_admin import db_admin_bp


def register_blueprints(app):
    app.register_blueprint(predict_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(db_admin_bp)
  
