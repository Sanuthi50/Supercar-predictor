#!/usr/bin/env python3
"""
Database initialization script for SuperCar Prediction application
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from app.models import Base, User, CarPrediction
from config import Config

def init_database():
    """Initialize the database and create tables"""
    load_dotenv()
    
    # Get database configuration
    config = Config()
    db_url = config.DATABASE_URL
    
    print(f"Connecting to database: {db_url.split('@')[-1]}")
    
    try:
        # Create engine
        engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Create a default admin user
        create_default_user(engine)
        
        return True
        
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")
        return False

def create_default_user(engine):
    """Create a default admin user for testing"""
    from sqlalchemy.orm import sessionmaker
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_user = session.query(User).filter(User.username == 'admin').first()
        
        if not existing_user:
            # Create default admin user
            admin_user = User(
                username='admin',
                email='admin@supercar.com',
                first_name='Admin',
                last_name='User'
            )
            admin_user.set_password('admin123')
            
            session.add(admin_user)
            session.commit()
            print("Default admin user created:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@supercar.com")
        else:
            print("Admin user already exists")
            
    except Exception as e:
        session.rollback()
        print(f"Error creating default user: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    success = init_database()
    if success:
        print("Database initialization completed successfully!")
        print("\nTables created:")
        print("- users (for authentication)")
        print("- car_predictions (with user_id foreign key)")
        print("\nYou can now:")
        print("1. Register new users")
        print("2. Login with existing users")
        print("3. Make predictions (linked to users)")
    else:
        print("Database initialization failed!")
        exit(1) 