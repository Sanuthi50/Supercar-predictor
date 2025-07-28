// Index page JavaScript
// Note: This file uses shared authentication utilities from auth-utils.js

// Global state
let isInitialized = false;

// Initialize application
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Set initial loading state
        document.body.classList.add('loading');
        
        // Set up event listeners first
        setupEventListeners();
        
        // Initialize index page with authentication
        await initializeIndexPage();
        
        
        // Mark initialization as complete
        isInitialized = true;
    } catch (error) {
        console.error('Initialization error:', error);
    } finally {
        // Remove loading state
        document.body.classList.remove('loading');
    }
});

// Setup event listeners
function setupEventListeners() {
    // Car prediction form (only form remaining on index page)
    const carForm = document.getElementById('carForm');
    if (carForm) {
        carForm.addEventListener('submit', handlePrediction);
    }
}


// Index page specific authentication handling
async function initializeIndexPage() {
    const isAuthenticated = await checkAuthStatus();
    updateUIForAuthState(isAuthenticated);
    
    // Index page only shows prediction form
    if (isAuthenticated) {
        showPredictionForm();
    } else {
        // Redirect unauthenticated users to login with return URL
        const currentUrl = encodeURIComponent(window.location.href);
        window.location.href = `/auth/login?next=${currentUrl}`;
    }
    
    return isAuthenticated;
}

// updateUIForAuthState is now handled by shared auth-utils.js
function showPredictionForm() {
    if (!currentUser) {
        // Redirect to login with redirect back to prediction
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('show', 'prediction');
        window.location.href = `/auth/login?next=${encodeURIComponent(currentUrl.toString())}`;
        return;
    }
    
    // Ensure we have the prediction section
    const predictionSection = document.getElementById('predictionSection');
    if (!predictionSection) {
        console.error('Prediction section not found');
        return;
    }
    
    // Hide all sections and show prediction
    hideAllSections();
    predictionSection.style.display = 'block';
    
    // Update URL without page reload
    const url = new URL(window.location);
    url.searchParams.set('show', 'prediction');
    window.history.pushState({}, '', url);
}

function hideAllSections() {
    const predictionSection = document.getElementById('predictionSection');
    if (predictionSection) predictionSection.style.display = 'none';
}

// Prediction functions
async function handlePrediction(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {};
    
    // Handle regular form fields
    for (let [key, value] of formData.entries()) {
        if (key === 'carbon_fiber_body' || key === 'aero_package' || 
            key === 'limited_edition' || key === 'has_warranty' || 
            key === 'non_original_parts' || key === 'damage') {
            data[key] = 1; // Checkbox checked = 1
        } else {
            data[key] = value;
        }
    }
    
    // Handle unchecked checkboxes (set to 0)
    const checkboxes = ['carbon_fiber_body', 'aero_package', 'limited_edition', 
                      'has_warranty', 'non_original_parts', 'damage'];
    checkboxes.forEach(checkbox => {
        if (!(checkbox in data)) {
            data[checkbox] = 0;
        }
    });
    
    // Convert numeric fields to appropriate types
    const intFields = ['year', 'horsepower', 'torque', 'weight_kg', 'top_speed_mph', 
                     'num_doors', 'mileage', 'num_owners', 'warranty_years'];
    const floatFields = ['zero_to_60_s', 'damage_cost'];
    
    intFields.forEach(field => {
        if (data[field] && data[field] !== '') {
            data[field] = parseInt(data[field]);
        } else {
            data[field] = 0; // Default value for empty fields
        }
    });
    
    floatFields.forEach(field => {
        if (data[field] && data[field] !== '') {
            data[field] = parseFloat(data[field]);
        } else {
            data[field] = 0.0; // Default value for empty fields
        }
    });
    
    // Validate required fields
    const requiredFields = ['year', 'brand', 'model'];
    const missingFields = requiredFields.filter(field => !data[field] || data[field] === '');
    
    if (missingFields.length > 0) {
        showError(`Missing required fields: ${missingFields.join(', ')}`);
        return;
    }
    
    // Make prediction API call
    await makePrediction(data);
}

// Make API request to predict
async function makePrediction(formData) {
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Include session cookies
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || result.error || `HTTP error! status: ${response.status}`);
        }
        
        if (result.success) {
            showPrediction(result);
        } else {
            throw new Error(result.message || 'Prediction failed');
        }
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError(`Failed to get prediction: ${error.message}`);
    }
}

// Show prediction result
function showPrediction(data) {
    hideAllResults();
    const priceElement = document.getElementById('predictedPrice');
    const detailsElement = document.getElementById('predictionDetails');
    
    // Format price with animation
    const price = data.predicted_price;
    priceElement.textContent = `$${price.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    })}`;
    
    // Show details using input_data from API response
    const inputData = data.input_data || {};
    detailsElement.innerHTML = `
        <strong>${inputData.year || 'Unknown'} ${inputData.brand || 'Unknown'} ${inputData.model || 'Unknown'}</strong><br>
        Mileage: ${inputData.mileage ? inputData.mileage.toLocaleString() + ' miles' : 'Not provided'}<br>
        Horsepower: ${inputData.horsepower || 'Not provided'} hp<br>
        Engine: ${inputData.engine_config || 'Not provided'}
    `;
    
    document.getElementById('predictionResult').style.display = 'block';
    document.getElementById('predictionResult').scrollIntoView({ behavior: 'smooth' });
}

// Utility functions
function hideAllResults() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('predictionResult').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
}

function showError(message) {
    hideAllResults();
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorMessage').style.display = 'block';
    document.getElementById('errorMessage').scrollIntoView({ behavior: 'smooth' });
}

function showSuccess(message) {
    // For now, just show as error but with different styling
    showError(message);
}

function showLoading() {
    hideAllResults();
    document.getElementById('loading').style.display = 'block';
    document.getElementById('loading').scrollIntoView({ behavior: 'smooth' });
}

// Test API connection
async function testConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('API Health Check:', data);
        // Check if status is healthy and model is loaded
        return data.status === 'healthy' && data.model === 'loaded';
    } catch (error) {
        console.error('API connection failed:', error);
        return false;
    }
}

// Test API connection on page load
window.addEventListener('load', async function() {
    const isConnected = await testConnection();
    if (!isConnected) {
        console.warn('API server is not running or model is not loaded. Please start the backend server.');
    }
});