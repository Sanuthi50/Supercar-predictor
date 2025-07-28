// Home page JavaScript
// Note: This file uses shared authentication utilities from auth-utils.js

// Initialize application
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Set initial loading state
        document.body.classList.add('loading');
        
        // Check authentication status using shared function
        const isAuthenticated = await checkAuthStatus();
        
        // Update UI based on authentication state
        updateUIForAuthState(isAuthenticated);
        
        // Handle home page specific UI
        handleHomePageUI(isAuthenticated);
        
    } catch (error) {
        console.error('Home page initialization error:', error);
    } finally {
        // Remove loading state
        document.body.classList.remove('loading');
    }
});

// Home page specific UI handling
function handleHomePageUI(isAuthenticated) {
    const welcomeSection = document.getElementById('welcomeSection');
    
    if (welcomeSection) {
        if (isAuthenticated) {
            // For authenticated users, show welcome section with user-specific content
            welcomeSection.style.display = 'block';
            // Could customize welcome message here if needed
        } else {
            // For unauthenticated users, show welcome section with login/register prompts
            welcomeSection.style.display = 'block';
        }
    }
}

// Navigation functions specific to home page
function showPredictionForm() {
    if (!currentUser) {
        // Redirect to dedicated login page with return URL
        window.location.href = '/auth/login?next=' + encodeURIComponent('/');
        return;
    }
    // Redirect to main prediction page
    window.location.href = '/';
}

// Test API connection on page load
window.addEventListener('load', async function() {
    const isConnected = await testConnection();
    if (!isConnected) {
        console.warn('API server is not running or model is not loaded. Please start the backend server.');
    }
});
