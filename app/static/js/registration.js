// Registration page specific functionality

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const fieldIds = ['username', 'email', 'password', 'first_name', 'last_name'];
    
    // Add real-time validation
    addRealTimeValidation(fieldIds, 'register');
    
    // Handle form submission
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous errors
        clearAllErrors(fieldIds);
        
        // Get form data
        const formData = {
            username: document.getElementById('username').value.trim(),
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value,
            first_name: document.getElementById('first_name').value.trim() || undefined,
            last_name: document.getElementById('last_name').value.trim() || undefined
        };
        
        // Remove empty optional fields
        if (!formData.first_name) delete formData.first_name;
        if (!formData.last_name) delete formData.last_name;
        
        // Client-side validation
        const validation = validateForm(formData, 'register');
        if (!validation.isValid) {
            // Display validation errors
            Object.keys(validation.errors).forEach(fieldId => {
                showFieldError(fieldId, validation.errors[fieldId]);
            });
            return;
        }
        
        // Show loading state
        showLoadingState('registerForm', 'registerBtn');
        
        try {
            // Make API request
            const response = await makeApiRequest('/auth/register', formData);
            
            if (response.success) {
                // Show success message
                showSuccessMessage('Account created successfully! Redirecting to login...');
                
                // Clear form
                registerForm.reset();
                clearAllErrors(fieldIds);
                
                // Redirect to login page after short delay
                setTimeout(() => {
                    window.location.href = '/auth/login';
                }, 2000);
            } else {
                throw response;
            }
            
        } catch (error) {
            // Handle API errors
            handleApiError(error, fieldIds);
        } finally {
            // Hide loading state
            hideLoadingState('registerForm', 'registerBtn', 'Create Account');
        }
    });
    
    // Focus on username field when page loads
    const usernameField = document.getElementById('username');
    if (usernameField) {
        usernameField.focus();
    }
    
    // Handle Enter key in form fields
    fieldIds.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    registerForm.dispatchEvent(new Event('submit'));
                }
            });
            
            // Clear general errors when user starts typing
            field.addEventListener('input', function() {
                hideGeneralError();
            });
        }
    });
    
    // Add password strength indicator
    const passwordField = document.getElementById('password');
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }
});

/**
 * Update password strength indicator
 * @param {string} password - The password to evaluate
 */
function updatePasswordStrength(password) {
    // Remove existing strength indicator
    const existingIndicator = document.querySelector('.password-strength');
    if (existingIndicator) {
        existingIndicator.remove();
    }
    
    if (password.length === 0) return;
    
    const passwordField = document.getElementById('password');
    const strength = calculatePasswordStrength(password);
    
    // Create strength indicator
    const strengthDiv = document.createElement('div');
    strengthDiv.className = 'password-strength';
    strengthDiv.innerHTML = `
        <div class="strength-bar">
            <div class="strength-fill strength-${strength.level}" style="width: ${strength.percentage}%"></div>
        </div>
        <span class="strength-text">${strength.text}</span>
    `;
    
    // Add CSS for strength indicator if not already added
    if (!document.querySelector('#password-strength-styles')) {
        const style = document.createElement('style');
        style.id = 'password-strength-styles';
        style.textContent = `
            .password-strength {
                margin-top: 0.5rem;
            }
            .strength-bar {
                height: 4px;
                background-color: #e2e8f0;
                border-radius: 2px;
                overflow: hidden;
                margin-bottom: 0.25rem;
            }
            .strength-fill {
                height: 100%;
                transition: width 0.3s ease, background-color 0.3s ease;
            }
            .strength-weak { background-color: #e53e3e; }
            .strength-fair { background-color: #dd6b20; }
            .strength-good { background-color: #38a169; }
            .strength-strong { background-color: #2f855a; }
            .strength-text {
                font-size: 0.8rem;
                color: #718096;
            }
        `;
        document.head.appendChild(style);
    }
    
    passwordField.parentNode.appendChild(strengthDiv);
}

/**
 * Calculate password strength
 * @param {string} password - The password to evaluate
 * @returns {Object} - Strength information
 */
function calculatePasswordStrength(password) {
    let score = 0;
    let feedback = [];
    
    // Length check
    if (password.length >= 8) score += 25;
    else if (password.length >= 6) score += 10;
    else feedback.push('too short');
    
    // Character variety checks
    if (/[a-z]/.test(password)) score += 15;
    if (/[A-Z]/.test(password)) score += 15;
    if (/[0-9]/.test(password)) score += 15;
    if (/[^A-Za-z0-9]/.test(password)) score += 20;
    
    // Length bonus
    if (password.length >= 12) score += 10;
    
    let level, text;
    if (score < 30) {
        level = 'weak';
        text = 'Weak password';
    } else if (score < 60) {
        level = 'fair';
        text = 'Fair password';
    } else if (score < 80) {
        level = 'good';
        text = 'Good password';
    } else {
        level = 'strong';
        text = 'Strong password';
    }
    
    return {
        score,
        percentage: Math.min(score, 100),
        level,
        text,
        feedback
    };
}
