from flask import Blueprint, request, jsonify, g, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging
from ..database import SessionLocal
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    db_session = None
    
    # Validate request format
    if not request.is_json:
        return jsonify({
            'error': 'Invalid request format',
            'message': 'Request must be JSON',
            'error_code': 'INVALID_FORMAT',
            'request_id': g.get('request_id', 'unknown')
        }), 400
    
    try:
        # Parse JSON data
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'Empty request body',
                    'message': 'Request body cannot be empty',
                    'error_code': 'EMPTY_BODY',
                    'request_id': g.get('request_id', 'unknown')
                }), 400
        except Exception as json_error:
            logging.error(f"JSON parsing error in registration: {str(json_error)}")
            return jsonify({
                'error': 'Invalid JSON',
                'message': 'Request body contains invalid JSON',
                'error_code': 'INVALID_JSON',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate required fields with detailed checking
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip() if data.get('first_name') else None
        last_name = data.get('last_name', '').strip() if data.get('last_name') else None
        
        # Check for missing required fields
        if not username:
            return jsonify({
                'error': 'Missing username',
                'message': 'Username is required and cannot be empty',
                'error_code': 'MISSING_USERNAME',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if not email:
            return jsonify({
                'error': 'Missing email',
                'message': 'Email is required and cannot be empty',
                'error_code': 'MISSING_EMAIL',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if not password:
            return jsonify({
                'error': 'Missing password',
                'message': 'Password is required and cannot be empty',
                'error_code': 'MISSING_PASSWORD',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate input lengths
        if len(username) < 3:
            return jsonify({
                'error': 'Username too short',
                'message': 'Username must be at least 3 characters long',
                'error_code': 'USERNAME_TOO_SHORT',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if len(username) > 150:
            return jsonify({
                'error': 'Username too long',
                'message': 'Username cannot exceed 150 characters',
                'error_code': 'USERNAME_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({
                'error': 'Invalid email format',
                'message': 'Please provide a valid email address',
                'error_code': 'INVALID_EMAIL_FORMAT',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if len(email) > 254:  # RFC 5321 limit
            return jsonify({
                'error': 'Email too long',
                'message': 'Email address cannot exceed 254 characters',
                'error_code': 'EMAIL_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate password strength
        if len(password) < 6:
            return jsonify({
                'error': 'Password too short',
                'message': 'Password must be at least 6 characters long',
                'error_code': 'PASSWORD_TOO_SHORT',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if len(password) > 500:
            return jsonify({
                'error': 'Password too long',
                'message': 'Password cannot exceed 500 characters',
                'error_code': 'PASSWORD_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate optional name fields
        if first_name and len(first_name) > 100:
            return jsonify({
                'error': 'First name too long',
                'message': 'First name cannot exceed 100 characters',
                'error_code': 'FIRST_NAME_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if last_name and len(last_name) > 100:
            return jsonify({
                'error': 'Last name too long',
                'message': 'Last name cannot exceed 100 characters',
                'error_code': 'LAST_NAME_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate username format (alphanumeric and underscore only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return jsonify({
                'error': 'Invalid username format',
                'message': 'Username can only contain letters, numbers, and underscores',
                'error_code': 'INVALID_USERNAME_FORMAT',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Database operations
        try:
            db_session = SessionLocal()
        except Exception as db_error:
            logging.error(f"Database connection error during registration: {str(db_error)}")
            return jsonify({
                'error': 'Database connection failed',
                'message': 'Unable to connect to database. Please try again later.',
                'error_code': 'DB_CONNECTION_ERROR',
                'request_id': g.get('request_id', 'unknown')
            }), 503
        
        try:
            # Check if username already exists
            try:
                existing_user = db_session.query(User).filter(User.username == username).first()
            except Exception as query_error:
                logging.error(f"Database query error checking username: {str(query_error)}")
                return jsonify({
                    'error': 'Database query failed',
                    'message': 'Unable to verify username availability. Please try again later.',
                    'error_code': 'DB_QUERY_ERROR',
                    'request_id': g.get('request_id', 'unknown')
                }), 500
                
            if existing_user:
                logging.warning(f"Registration attempt with existing username: {username}")
                return jsonify({
                    'error': 'Username already exists',
                    'message': 'This username is already taken. Please choose a different username.',
                    'error_code': 'USERNAME_EXISTS',
                    'request_id': g.get('request_id', 'unknown')
                }), 409
            
            # Check if email already exists
            try:
                existing_email = db_session.query(User).filter(User.email == email).first()
            except Exception as query_error:
                logging.error(f"Database query error checking email: {str(query_error)}")
                return jsonify({
                    'error': 'Database query failed',
                    'message': 'Unable to verify email availability. Please try again later.',
                    'error_code': 'DB_QUERY_ERROR',
                    'request_id': g.get('request_id', 'unknown')
                }), 500
                
            if existing_email:
                logging.warning(f"Registration attempt with existing email: {email}")
                return jsonify({
                    'error': 'Email already exists',
                    'message': 'This email address is already registered. Please use a different email or try logging in.',
                    'error_code': 'EMAIL_EXISTS',
                    'request_id': g.get('request_id', 'unknown')
                }), 409
            
            # Create new user
            try:
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(password)
            except Exception as user_creation_error:
                logging.error(f"User object creation error: {str(user_creation_error)}")
                return jsonify({
                    'error': 'User creation failed',
                    'message': 'Unable to create user account. Please try again.',
                    'error_code': 'USER_CREATION_ERROR',
                    'request_id': g.get('request_id', 'unknown')
                }), 500
            
            # Save user to database
            try:
                db_session.add(user)
                db_session.commit()
            except Exception as save_error:
                db_session.rollback()
                logging.error(f"Database save error during registration: {str(save_error)}")
                return jsonify({
                    'error': 'Registration save failed',
                    'message': 'Unable to save user account. Please try again later.',
                    'error_code': 'DB_SAVE_ERROR',
                    'request_id': g.get('request_id', 'unknown')
                }), 500
            
            logging.info(f"Successfully registered new user: {username}")
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user': user.to_dict(),
                'request_id': g.get('request_id', 'unknown')
            }), 201
            
        except Exception as db_operation_error:
            logging.error(f"Database operation error during registration: {str(db_operation_error)}")
            if db_session:
                try:
                    db_session.rollback()
                except:
                    pass
            return jsonify({
                'error': 'Database operation failed',
                'message': 'Unable to complete registration. Please try again later.',
                'error_code': 'DB_OPERATION_ERROR',
                'request_id': g.get('request_id', 'unknown')
            }), 500
        
    except Exception as e:
        logging.error(f"Unexpected registration error: {str(e)}")
        if db_session:
            try:
                db_session.rollback()
            except:
                pass
        return jsonify({
            'error': 'Registration failed',
            'message': 'An unexpected error occurred during registration. Please try again later.',
            'error_code': 'UNEXPECTED_ERROR',
            'request_id': g.get('request_id', 'unknown')
        }), 500
    finally:
        if db_session:
            try:
                db_session.close()
            except Exception as close_error:
                logging.error(f"Error closing database session: {str(close_error)}")

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    db_session = None
    
    # Validate request format
    if not request.is_json:
        return jsonify({
            'error': 'Invalid request format',
            'message': 'Request must be JSON',
            'error_code': 'INVALID_FORMAT',
            'request_id': g.get('request_id', 'unknown')
        }), 400
    
    try:
        # Parse JSON data
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'Empty request body',
                    'message': 'Request body cannot be empty',
                    'error_code': 'EMPTY_BODY',
                    'request_id': g.get('request_id', 'unknown')
                }), 400
        except Exception as json_error:
            logging.error(f"JSON parsing error: {str(json_error)}")
            return jsonify({
                'error': 'Invalid JSON',
                'message': 'Request body contains invalid JSON',
                'error_code': 'INVALID_JSON',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate required fields
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username:
            return jsonify({
                'error': 'Missing username',
                'message': 'Username is required and cannot be empty',
                'error_code': 'MISSING_USERNAME',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if not password:
            return jsonify({
                'error': 'Missing password',
                'message': 'Password is required and cannot be empty',
                'error_code': 'MISSING_PASSWORD',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Validate input lengths
        if len(username) > 150:
            return jsonify({
                'error': 'Username too long',
                'message': 'Username cannot exceed 150 characters',
                'error_code': 'USERNAME_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
            
        if len(password) > 500:
            return jsonify({
                'error': 'Password too long',
                'message': 'Password cannot exceed 500 characters',
                'error_code': 'PASSWORD_TOO_LONG',
                'request_id': g.get('request_id', 'unknown')
            }), 400
        
        # Database operations
        try:
            db_session = SessionLocal()
        except Exception as db_error:
            logging.error(f"Database connection error: {str(db_error)}")
            return jsonify({
                'error': 'Database connection failed',
                'message': 'Unable to connect to database. Please try again later.',
                'error_code': 'DB_CONNECTION_ERROR',
                'request_id': g.get('request_id', 'unknown')
            }), 503
        
        try:
            # Find user by username
            user = db_session.query(User).filter(User.username == username).first()
            
            # Check if user exists
            if not user:
                logging.warning(f"Login attempt with non-existent username: {username}")
                return jsonify({
                    'error': 'Invalid credentials',
                    'message': 'Username or password is incorrect',
                    'error_code': 'INVALID_CREDENTIALS',
                    'request_id': g.get('request_id', 'unknown')
                }), 401
            
            # Check password
            try:
                password_valid = user.check_password(password)
            except Exception as pwd_error:
                logging.error(f"Password verification error for user {username}: {str(pwd_error)}")
                return jsonify({
                    'error': 'Authentication error',
                    'message': 'Unable to verify credentials. Please try again.',
                    'error_code': 'AUTH_VERIFICATION_ERROR',
                    'request_id': g.get('request_id', 'unknown')
                }), 500
            
            if not password_valid:
                logging.warning(f"Invalid password attempt for user: {username}")
                return jsonify({
                    'error': 'Invalid credentials',
                    'message': 'Username or password is incorrect',
                    'error_code': 'INVALID_CREDENTIALS',
                    'request_id': g.get('request_id', 'unknown')
                }), 401
            
            # Check if account is active
            if not user.is_active:
                logging.warning(f"Login attempt on disabled account: {username}")
                return jsonify({
                    'error': 'Account disabled',
                    'message': 'Your account has been disabled. Please contact support.',
                    'error_code': 'ACCOUNT_DISABLED',
                    'request_id': g.get('request_id', 'unknown')
                }), 403
            
            # Update last login timestamp
            try:
                user.last_login = datetime.utcnow()
                db_session.commit()
            except Exception as update_error:
                logging.error(f"Failed to update last login for user {username}: {str(update_error)}")
                db_session.rollback()
            
            # Store user in session
            try:
                session['user_id'] = user.id
                session['username'] = user.username
            except Exception as session_error:
                logging.error(f"Session creation error for user {username}: {str(session_error)}")
                return jsonify({
                    'error': 'Session creation failed',
                    'message': 'Login successful but session could not be created. Please try again.',
                    'error_code': 'SESSION_ERROR',
                    'request_id': g.get('request_id', 'unknown')
                }), 500
            
            logging.info(f"Successful login for user: {username}")
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict(),
                'request_id': g.get('request_id', 'unknown')
            })
            
        except Exception as query_error:
            logging.error(f"Database query error during login: {str(query_error)}")
            if db_session:
                db_session.rollback()
            return jsonify({
                'error': 'Database query failed',
                'message': 'Unable to process login request. Please try again later.',
                'error_code': 'DB_QUERY_ERROR',
                'request_id': g.get('request_id', 'unknown')
            }), 500
        
    except Exception as e:
        logging.error(f"Unexpected login error: {str(e)}")
        if db_session:
            try:
                db_session.rollback()
            except:
                pass
        return jsonify({
            'error': 'Login failed',
            'message': 'An unexpected error occurred. Please try again later.',
            'error_code': 'UNEXPECTED_ERROR',
            'request_id': g.get('request_id', 'unknown')
        }), 500
    finally:
        if db_session:
            try:
                db_session.close()
            except Exception as close_error:
                logging.error(f"Error closing database session: {str(close_error)}")

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logout successful',
            'request_id': g.get('request_id', 'unknown')
        })
        
    except Exception as e:
        logging.error(f"Logout error: {str(e)}")
        return jsonify({
            'error': 'Logout failed',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 500

@auth_bp.route('/auth/profile', methods=['GET'])
def get_profile():
    """Get current user profile"""
    db_session = None
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please login to access your profile',
                'request_id': g.get('request_id', 'unknown')
            }), 401
        
        db_session = SessionLocal()
        user = db_session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'User account not found',
                'request_id': g.get('request_id', 'unknown')
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'request_id': g.get('request_id', 'unknown')
        })
        
    except Exception as e:
        logging.error(f"Profile error: {str(e)}")
        return jsonify({
            'error': 'Failed to get profile',
            'message': str(e),
            'request_id': g.get('request_id', 'unknown')
        }), 500
    finally:
        if db_session:
            db_session.close()

@auth_bp.route('/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    db_session = None
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'authenticated': False,
                'request_id': g.get('request_id', 'unknown')
            })
        
        db_session = SessionLocal()
        user = db_session.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            return jsonify({
                'authenticated': False,
                'request_id': g.get('request_id', 'unknown')
            })
        
        return jsonify({
            'authenticated': True,
            'user': user.to_dict(),
            'request_id': g.get('request_id', 'unknown')
        })
        
    except Exception as e:
        logging.error(f"Auth check error: {str(e)}")
        return jsonify({
            'authenticated': False,
            'error': str(e),
            'request_id': g.get('request_id', 'unknown')
        })
    finally:
        if db_session:
            db_session.close()

# Page routes for serving HTML templates
@auth_bp.route('/auth/login')
def login_page():
    """Serve the login page"""
    return render_template('login.html')

@auth_bp.route('/auth/register')
def register_page():
    """Serve the registration page"""
    return render_template('registration.html')