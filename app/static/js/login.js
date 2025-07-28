// Login page specific functionality

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const fieldIds = ['username', 'password'];
    
    // Add real-time validation
    addRealTimeValidation(fieldIds, 'login');
    
    // Handle form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous errors
        clearAllErrors(fieldIds);
        
        // Get form data
        const formData = {
            username: document.getElementById('username').value.trim(),
            password: document.getElementById('password').value
        };
        
        // Client-side validation
        const validation = validateForm(formData, 'login');
        if (!validation.isValid) {
            // Display validation errors
            Object.keys(validation.errors).forEach(fieldId => {
                showFieldError(fieldId, validation.errors[fieldId]);
            });
            return;
        }
        
        // Show loading state
        showLoadingState('loginForm', 'loginBtn');
        
        try {
            console.log('Submitting login form with data:', formData);
            
            // Make API request
            const response = await makeApiRequest('/auth/login', formData);
            
            console.log('Login response received:', response);
            
            if (response.success) {
                // Show success message
                showSuccessMessage('Login successful! Redirecting...');
                
                // Check for return URL parameter, otherwise redirect to main page
                const urlParams = new URLSearchParams(window.location.search);
                let returnUrl = urlParams.get('next') || '/';
                
                // Add from=login parameter to help with auth timing
                const returnUrlObj = new URL(returnUrl, window.location.origin);
                returnUrlObj.searchParams.set('from', 'login');
                returnUrl = returnUrlObj.toString();
                
                setTimeout(() => {
                    window.location.href = returnUrl;
                }, 1500);
            } else {
                console.warn('Login response indicates failure:', response);
                throw response;
            }
            
        } catch (error) {
            console.error('Login form caught error:', error);
            
            // Handle API errors
            handleApiError(error, fieldIds);
            
            // Additional fallback for debugging
            if (!document.getElementById('generalError').style.display || 
                document.getElementById('generalError').style.display === 'none') {
                console.warn('Error not displayed, showing fallback message');
                showGeneralError(error.message || 'Login failed. Please check your credentials and try again.');
            }
        } finally {
            // Hide loading state
            hideLoadingState('loginForm', 'loginBtn', 'Sign In');
        }
    });
    
    // Focus on username field when page loads
    const usernameField = document.getElementById('username');
    if (usernameField) {
        usernameField.focus();
    }
    
    // Handle Enter key in password field
    const passwordField = document.getElementById('password');
    if (passwordField) {
        passwordField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                loginForm.dispatchEvent(new Event('submit'));
            }
        });
    }
    
    // Clear errors when user starts typing
    fieldIds.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', function() {
                hideGeneralError();
            });
        }
    });
});
