from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Base

engine = None
SessionLocal = None

def init_db(app):
    """Initialize database connection"""
    global engine, SessionLocal
    
    try:
        db_url = app.config['DATABASE_URL']
        app.logger.info(f"Attempting to connect to database at: {db_url.split('@')[-1]}")
        engine = create_engine(
            app.config['DATABASE_URL'],
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        app.logger.info("Database setup completed successfully!")
        return True
        
    except Exception as e:
        app.logger.error(f"Database setup failed: {str(e)}")
        return False

def get_db_session():
    """Get a database session with context management"""
    if SessionLocal is None:
        return None
    
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise
    finally:
        session.close()