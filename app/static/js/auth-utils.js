// Shared Authentication Utilities
// Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';

// Global state
let currentUser = null;
let isAuthCheckComplete = false;

// Shared authentication functions
async function checkAuthStatus(retryCount = 0) {
    try {
        console.log(`Checking auth status (attempt ${retryCount + 1})...`);
        
        const response = await fetch(`${API_BASE_URL}/auth/check`, {
            credentials: 'include' // Include session cookies
        });
        
        if (!response.ok) throw new Error(`Auth check failed with status ${response.status}`);
        
        const data = await response.json();
        console.log('Auth check response:', data);
        
        if (data.authenticated && data.user) {
            currentUser = data.user;
            console.log('User authenticated:', currentUser.username);
            return true;
        } else {
            currentUser = null;
            console.log('User not authenticated');
            
            // If we just came from login and auth failed, retry once after a short delay
            if (retryCount === 0 && window.location.search.includes('from=login')) {
                console.log('Retrying auth check after login redirect...');
                await new Promise(resolve => setTimeout(resolve, 1000));
                return await checkAuthStatus(1);
            }
            
            return false;
        }
        
    } catch (error) {
        console.error('Auth check failed:', error);
        currentUser = null;
        
        // Retry once on network error
        if (retryCount === 0) {
            console.log('Retrying auth check after error...');
            await new Promise(resolve => setTimeout(resolve, 500));
            return await checkAuthStatus(1);
        }
        
        return false;
    } finally {
        isAuthCheckComplete = true;
    }
}

// Unified UI update function that works for both pages
function updateUIForAuthState(isAuthenticated) {
    const navAuth = document.getElementById('navAuth');
    const navUser = document.getElementById('navUser');
    const userInfo = document.getElementById('userInfo');
    
    // Update navigation based on auth state
    if (navAuth) navAuth.style.display = isAuthenticated ? 'none' : 'flex';
    if (navUser) navUser.style.display = isAuthenticated ? 'flex' : 'none';
    
    // Update user info if authenticated
    if (isAuthenticated && currentUser && userInfo) {
        userInfo.textContent = `Welcome, ${currentUser.username}`;
    }
}


// Shared logout function
async function logout() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include' // Include session cookies
        });
        
        if (response.ok) {
            currentUser = null;
            updateUIForAuthState(false);
            // Redirect to home page after logout
            window.location.href = '/home';
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
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


