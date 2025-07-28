// Common authentication utilities and functions

/**
 * Display error message for a specific field
 * @param {string} fieldId - The ID of the field
 * @param {string} message - Error message to display
 */
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(fieldId + 'Error');
    
    if (field) {
        field.classList.add('error');
        field.classList.remove('success');
        // Add focus to the field with error
        field.focus();
    }
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'flex';
        // Add animation class for better UX
        errorElement.classList.add('error-show');
        
        // Scroll to the error if it's not visible
        setTimeout(() => {
            errorElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'nearest'
            });
        }, 100);
    } else {
        console.warn(`Error element not found for field: ${fieldId}`);
    }
}

/**
 * Clear error message for a specific field
 * @param {string} fieldId - The ID of the field
 */
function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(fieldId + 'Error');
    
    if (field) {
        field.classList.remove('error');
    }
    
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
        errorElement.classList.remove('error-show');
    }
}

/**
 * Mark field as valid
 * @param {string} fieldId - The ID of the field
 */
function markFieldSuccess(fieldId) {
    const field = document.getElementById(fieldId);
    
    if (field) {
        field.classList.remove('error');
        field.classList.add('success');
    }
    
    clearFieldError(fieldId);
}

/**
 * Display general error message
 * @param {string} message - Error message to display
 */
function showGeneralError(message) {
    const errorContainer = document.getElementById('generalError');
    const errorText = document.getElementById('errorText');
    
    if (errorContainer && errorText) {
        errorText.textContent = message;
        errorContainer.style.display = 'block';
        errorContainer.classList.add('error-show');
        
        // Scroll to the error message
        setTimeout(() => {
            errorContainer.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'nearest'
            });
        }, 100);
        
        // Add shake animation for attention
        errorContainer.classList.add('shake');
        setTimeout(() => {
            errorContainer.classList.remove('shake');
        }, 600);
    } else {
        console.warn('General error container not found');
        // Fallback: show alert if DOM elements not found
        alert(`Error: ${message}`);
    }
}

/**
 * Hide general error message
 */
function hideGeneralError() {
    const errorContainer = document.getElementById('generalError');
    if (errorContainer) {
        errorContainer.style.display = 'none';
        errorContainer.classList.remove('error-show', 'shake');
    }
}

/**
 * Show loading state for form
 * @param {string} formId - The ID of the form
 * @param {string} buttonId - The ID of the submit button
 */
function showLoadingState(formId, buttonId) {
    const form = document.getElementById(formId);
    const button = document.getElementById(buttonId);
    const btnText = button.querySelector('.btn-text');
    const btnSpinner = button.querySelector('.btn-spinner');
    
    if (form) form.classList.add('loading');
    if (button) button.disabled = true;
    if (btnSpinner) btnSpinner.style.display = 'block';
    if (btnText) btnText.textContent = 'Processing...';
}

/**
 * Hide loading state for form
 * @param {string} formId - The ID of the form
 * @param {string} buttonId - The ID of the submit button
 * @param {string} originalText - Original button text
 */
function hideLoadingState(formId, buttonId, originalText) {
    const form = document.getElementById(formId);
    const button = document.getElementById(buttonId);
    const btnText = button.querySelector('.btn-text');
    const btnSpinner = button.querySelector('.btn-spinner');
    
    if (form) form.classList.remove('loading');
    if (button) button.disabled = false;
    if (btnSpinner) btnSpinner.style.display = 'none';
    if (btnText) btnText.textContent = originalText;
}

/**
 * Clear all form errors
 * @param {Array} fieldIds - Array of field IDs to clear
 */
function clearAllErrors(fieldIds) {
    fieldIds.forEach(fieldId => clearFieldError(fieldId));
    hideGeneralError();
}

/**
 * Handle API errors and display appropriate messages
 * @param {Object} error - Error response from API
 * @param {Array} fieldIds - Array of field IDs for clearing errors
 */
function handleApiError(error, fieldIds = []) {
    console.error('API Error:', error);
    
    // Clear previous errors
    clearAllErrors(fieldIds);
    
    if (error.error_code) {
        switch (error.error_code) {
            // Format and JSON errors
            case 'INVALID_FORMAT':
            case 'EMPTY_BODY':
            case 'INVALID_JSON':
                showGeneralError(error.message);
                break;
                
            // Username errors
            case 'MISSING_USERNAME':
            case 'USERNAME_TOO_SHORT':
            case 'USERNAME_TOO_LONG':
            case 'INVALID_USERNAME_FORMAT':
            case 'USERNAME_EXISTS':
                showFieldError('username', error.message);
                break;
                
            // Email errors
            case 'MISSING_EMAIL':
            case 'INVALID_EMAIL_FORMAT':
            case 'EMAIL_TOO_LONG':
            case 'EMAIL_EXISTS':
                showFieldError('email', error.message);
                break;
                
            // Password errors
            case 'MISSING_PASSWORD':
            case 'PASSWORD_TOO_SHORT':
            case 'PASSWORD_TOO_LONG':
                showFieldError('password', error.message);
                break;
                
            // Name field errors
            case 'FIRST_NAME_TOO_LONG':
                showFieldError('first_name', error.message);
                break;
                
            case 'LAST_NAME_TOO_LONG':
                showFieldError('last_name', error.message);
                break;
                
            // Authentication errors
            case 'INVALID_CREDENTIALS':
                showGeneralError(error.message);
                // Also highlight username and password fields
                document.getElementById('username')?.classList.add('error');
                document.getElementById('password')?.classList.add('error');
                break;
                
            case 'ACCOUNT_DISABLED':
                showGeneralError(error.message);
                break;
                
            case 'AUTH_VERIFICATION_ERROR':
                showGeneralError(error.message);
                break;
                
            // Database and system errors
            case 'DB_CONNECTION_ERROR':
            case 'DB_QUERY_ERROR':
            case 'DB_SAVE_ERROR':
            case 'DB_OPERATION_ERROR':
                showGeneralError(error.message);
                break;
                
            case 'USER_CREATION_ERROR':
                showGeneralError(error.message);
                break;
                
            case 'SESSION_ERROR':
                showGeneralError(error.message);
                break;
                
            case 'NETWORK_ERROR':
                showGeneralError(error.message);
                break;
                
            case 'UNEXPECTED_ERROR':
                showGeneralError(error.message);
                break;
                
            default:
                console.warn('Unhandled error code:', error.error_code);
                showGeneralError(error.message || 'An unexpected error occurred. Please try again.');
        }
    } else {
        // Fallback for errors without error codes
        showGeneralError(error.message || 'An unexpected error occurred. Please try again.');
    }
}

/**
 * Make API request with error handling
 * @param {string} url - API endpoint URL
 * @param {Object} data - Data to send
 * @param {string} method - HTTP method (default: POST)
 * @returns {Promise} - Promise that resolves with response data
 */
async function makeApiRequest(url, data, method = 'POST') {
    try {
        console.log(`Making ${method} request to ${url}`, data);
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        console.log(`Response status: ${response.status}`);
        
        let result;
        try {
            result = await response.json();
            console.log('Response data:', result);
        } catch (parseError) {
            console.error('Failed to parse JSON response:', parseError);
            throw {
                error: 'Invalid Response',
                message: 'Server returned an invalid response. Please try again.',
                error_code: 'INVALID_RESPONSE',
                status: response.status
            };
        }
        
        if (!response.ok) {
            // Ensure the error object has the required structure
            const errorObj = {
                error: result.error || 'Request Failed',
                message: result.message || `Request failed with status ${response.status}`,
                error_code: result.error_code || 'HTTP_ERROR',
                status: response.status,
                ...result // Spread any additional properties from the response
            };
            console.error('API Error:', errorObj);
            throw errorObj;
        }
        
        return result;
    } catch (error) {
        // If it's a network error or fetch error
        if (error instanceof TypeError || error.name === 'TypeError') {
            const networkError = {
                error: 'Network Error',
                message: 'Unable to connect to the server. Please check your connection and try again.',
                error_code: 'NETWORK_ERROR'
            };
            console.error('Network Error:', networkError);
            throw networkError;
        }
        
        // If it's already a properly formatted error, re-throw it
        if (error.error || error.message || error.error_code) {
            throw error;
        }
        
        // Fallback for unexpected errors
        const unexpectedError = {
            error: 'Unexpected Error',
            message: 'An unexpected error occurred. Please try again.',
            error_code: 'UNEXPECTED_ERROR',
            originalError: error.toString()
        };
        console.error('Unexpected Error:', unexpectedError);
        throw unexpectedError;
    }
}

/**
 * Validate form fields on the client side
 * @param {Object} formData - Form data to validate
 * @param {string} formType - Type of form ('login' or 'register')
 * @returns {Object} - Validation result with isValid and errors
 */
function validateForm(formData, formType) {
    const errors = {};
    let isValid = true;
    
    // Username validation
    if (!formData.username || formData.username.trim().length === 0) {
        errors.username = 'Username is required';
        isValid = false;
    } else if (formData.username.trim().length < 3) {
        errors.username = 'Username must be at least 3 characters long';
        isValid = false;
    } else if (formData.username.trim().length > 150) {
        errors.username = 'Username cannot exceed 150 characters';
        isValid = false;
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username.trim())) {
        errors.username = 'Username can only contain letters, numbers, and underscores';
        isValid = false;
    }
    
    // Password validation
    if (!formData.password || formData.password.length === 0) {
        errors.password = 'Password is required';
        isValid = false;
    } else if (formData.password.length < 6) {
        errors.password = 'Password must be at least 6 characters long';
        isValid = false;
    } else if (formData.password.length > 500) {
        errors.password = 'Password cannot exceed 500 characters';
        isValid = false;
    }
    
    // Registration-specific validation
    if (formType === 'register') {
        // Email validation
        if (!formData.email || formData.email.trim().length === 0) {
            errors.email = 'Email is required';
            isValid = false;
        } else {
            const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailPattern.test(formData.email.trim())) {
                errors.email = 'Please provide a valid email address';
                isValid = false;
            } else if (formData.email.trim().length > 254) {
                errors.email = 'Email address cannot exceed 254 characters';
                isValid = false;
            }
        }
        
        // Optional name fields validation
        if (formData.first_name && formData.first_name.trim().length > 100) {
            errors.first_name = 'First name cannot exceed 100 characters';
            isValid = false;
        }
        
        if (formData.last_name && formData.last_name.trim().length > 100) {
            errors.last_name = 'Last name cannot exceed 100 characters';
            isValid = false;
        }
    }
    
    return { isValid, errors };
}

/**
 * Add real-time validation to form fields
 * @param {Array} fieldIds - Array of field IDs to add validation to
 * @param {string} formType - Type of form ('login' or 'register')
 */
function addRealTimeValidation(fieldIds, formType) {
    fieldIds.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('blur', function() {
                const formData = {};
                fieldIds.forEach(id => {
                    const element = document.getElementById(id);
                    if (element) {
                        formData[element.name] = element.value;
                    }
                });
                
                const validation = validateForm(formData, formType);
                
                if (validation.errors[fieldId]) {
                    showFieldError(fieldId, validation.errors[fieldId]);
                } else if (field.value.trim()) {
                    markFieldSuccess(fieldId);
                } else {
                    clearFieldError(fieldId);
                }
            });
            
            field.addEventListener('input', function() {
                if (field.classList.contains('error')) {
                    clearFieldError(fieldId);
                }
            });
        }
    });
}

/**
 * Show success message
 * @param {string} message - Success message to display
 */
function showSuccessMessage(message) {
    // Remove any existing success messages
    const existingSuccess = document.querySelector('.success-message');
    if (existingSuccess) {
        existingSuccess.remove();
    }
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `<strong>Success:</strong> ${message}`;
    
    const form = document.querySelector('.auth-form');
    if (form) {
        form.appendChild(successDiv);
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}
