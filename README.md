# SuperCar Price Prediction Application

A Flask-based web application for predicting supercar prices using machine learning.

## Features

- 🚗 Supercar price prediction using ML models
- 👤 User authentication and registration system
- 📊 RESTful API endpoints
- 🗄️ PostgreSQL database integration
- 📈 Prediction history and statistics
- 🔍 Health monitoring and diagnostics
- 🎨 Minimal black and white elegant design

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip (Python package manager)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd SuperCarPrediction
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=car_predictions

   # Model Configuration
   MODEL_PATH=supercar_price_prediction_model.pkl

   # Application Configuration
   ENVIRONMENT=development
   PORT=5000
   ```

5. **Set up PostgreSQL database**:
   - Install PostgreSQL if not already installed
   - Create a database named `car_predictions`
   - Update the `.env` file with your database credentials

6. **Initialize the database**:
   ```bash
   python init_db.py
   ```

7. **Add foreign key constraints** (optional but recommended):
   ```bash
   python create_foreign_key.py
   ```

## Running the Application

### Development Mode
```bash
python run.py
```

The application will be available at `[http://localhost:5000](http://127.0.0.1:5000/home)`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/profile` - Get current user profile
- `GET /auth/check` - Check authentication status

### Health Check
- `GET /health` - Check application health and status

### Predictions
- `POST /` - Make a car price prediction
- `GET /predictions/history` - Get prediction history
- `GET /predictions/stats` - Get prediction statistics

### Get Prediction History
```bash
curl http://localhost:5000/predictions/history?limit=10
```

## Project Structure

```
SuperCarPrediction/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models (User, CarPrediction)
│   ├── database.py          # Database configuration
│   ├── ml.py               # Machine learning utilities
│   ├── utils.py            # Utility functions
│   ├── static/             # Static files
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript files
│   ├── templates/          # HTML templates
│   └── routes/             # API route blueprints
│       ├── health.py       # Health check endpoints
│       ├── predict.py      # Prediction endpoints
│       ├── history.py      # History endpoints
│       ├── stats.py        # Statistics endpoints
│       ├── auth.py         # Authentication endpoints
│       ├── db_admin.py     # Database admin endpoints
│       └── main.py         # Main routes
├── config.py               # Configuration settings
├── run.py                  # Application entry point
├── init_db.py             # Database initialization
├── .env                   # EnvironmentFile 
├── supercar_price_prediction_model.pkl # Machine Learning model's pkl file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```
### Common Issues

1. **Database Connection Failed**:
   - Ensure PostgreSQL is running
   - Check database credentials in `.env` file
   - Verify database exists

2. **Model Loading Failed**:
   - Ensure the model file exists at the specified path
   - Check file permissions

3. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Port Already in Use**:
   - Change the port in `.env` file
   - Or kill the process using the port

### Logs

Application logs are written to `app.log` in the root directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 
