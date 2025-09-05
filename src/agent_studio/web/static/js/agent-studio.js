/**
 * Agent Studio JavaScript Library
 * 
 * Provides common functionality for the Agent Studio web interface including
 * API communication, UI utilities, and shared components.
 */

// Global configuration
const AgentStudioConfig = {
    apiBaseUrl: '/api',
    version: '1.0.0',
    debug: false
};

// API Client
class AgentStudioAPI {
    static baseURL = AgentStudioConfig.apiBaseUrl;
    
    static async request(method, endpoint, data = null, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        // Add authentication token if available
        const token = this.getAuthToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Add request body for POST/PUT requests
        if (data && ['POST', 'PUT', 'PATCH'].includes(config.method)) {
            config.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, config);
            
            // Handle non-JSON responses
            const contentType = response.headers.get('content-type');
            let responseData;
            
            if (contentType && contentType.includes('application/json')) {
                responseData = await response.json();
            } else {
                responseData = await response.text();
            }
            
            if (!response.ok) {
                throw new APIError(response.status, responseData.error || responseData || 'Request failed');
            }
            
            return { data: responseData, status: response.status };
        } catch (error) {
            if (error instanceof APIError) {
                throw error;
            }
            throw new APIError(0, `Network error: ${error.message}`);
        }
    }
    
    static async get(endpoint, options = {}) {
        return this.request('GET', endpoint, null, options);
    }
    
    static async post(endpoint, data, options = {}) {
        return this.request('POST', endpoint, data, options);
    }
    
    static async put(endpoint, data, options = {}) {
        return this.request('PUT', endpoint, data, options);
    }
    
    static async patch(endpoint, data, options = {}) {
        return this.request('PATCH', endpoint, data, options);
    }
    
    static async delete(endpoint, options = {}) {
        return this.request('DELETE', endpoint, null, options);
    }
    
    static getAuthToken() {
        return localStorage.getItem('agent_studio_token') || sessionStorage.getItem('agent_studio_token');
    }
    
    static setAuthToken(token, persistent = false) {
        if (persistent) {
            localStorage.setItem('agent_studio_token', token);
        } else {
            sessionStorage.setItem('agent_studio_token', token);
        }
    }
    
    static clearAuthToken() {
        localStorage.removeItem('agent_studio_token');
        sessionStorage.removeItem('agent_studio_token');
    }
}

// Custom Error Class
class APIError extends Error {
    constructor(status, message) {
        super(message);
        this.name = 'APIError';
        this.status = status;
    }
}

// UI Utilities
class UIUtils {
    // Alert Management
    static showAlert(message, type = 'info', duration = 5000) {
        const alertsContainer = document.getElementById('alerts-container');
        if (!alertsContainer) return;
        
        const alertId = `alert-${Date.now()}`;
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
                <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        alertsContainer.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-dismiss after duration
        if (duration > 0) {
            setTimeout(() => {
                const alert = document.getElementById(alertId);
                if (alert) {
                    const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                    bsAlert.close();
                }
            }, duration);
        }
    }
    
    static getAlertIcon(type) {
        const icons = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle',
            primary: 'info-circle',
            secondary: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    // Loading States
    static showLoading(element, text = 'Loading...') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (!element) return;
        
        element.innerHTML = `
            <div class="d-flex align-items-center justify-content-center py-4">
                <div class="spinner-border text-primary me-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span>${text}</span>
            </div>
        `;
    }
    
    static hideLoading(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (!element) return;
        
        element.innerHTML = '';
    }
    
    // Form Utilities
    static getFormData(formElement) {
        const formData = new FormData(formElement);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                // Handle multiple values (checkboxes, etc.)
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        
        return data;
    }
    
    static validateForm(formElement) {
        const requiredFields = formElement.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    
    // Modal Utilities
    static showModal(modalId, options = {}) {
        const modalElement = document.getElementById(modalId);
        if (!modalElement) return null;
        
        const modal = new bootstrap.Modal(modalElement, options);
        modal.show();
        return modal;
    }
    
    static hideModal(modalId) {
        const modalElement = document.getElementById(modalId);
        if (!modalElement) return;
        
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
            modal.hide();
        }
    }
    
    // Confirmation Dialogs
    static async confirm(message, title = 'Confirm Action') {
        return new Promise((resolve) => {
            const modalHtml = `
                <div class="modal fade" id="confirmModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${title}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p>${message}</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="confirmCancel">Cancel</button>
                                <button type="button" class="btn btn-primary" id="confirmOk">Confirm</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remove existing modal if present
            const existingModal = document.getElementById('confirmModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            // Add modal to body
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            
            const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
            
            document.getElementById('confirmOk').addEventListener('click', () => {
                modal.hide();
                resolve(true);
            });
            
            document.getElementById('confirmCancel').addEventListener('click', () => {
                modal.hide();
                resolve(false);
            });
            
            // Clean up when modal is hidden
            document.getElementById('confirmModal').addEventListener('hidden.bs.modal', () => {
                document.getElementById('confirmModal').remove();
            });
            
            modal.show();
        });
    }
    
    // Utility Functions
    static formatDate(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString();
    }
    
    static formatDateTime(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleString();
    }
    
    static formatRelativeTime(dateString) {
        if (!dateString) return 'N/A';
        
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
        if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
        if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
        
        return this.formatDate(dateString);
    }
    
    static truncateText(text, maxLength = 100) {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    static capitalizeFirst(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
    
    static formatSpecialization(specialization) {
        if (!specialization) return '';
        return specialization.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
}

// Component Classes
class TagInput {
    constructor(element, options = {}) {
        this.element = typeof element === 'string' ? document.getElementById(element) : element;
        this.options = {
            placeholder: 'Add tags...',
            maxTags: 10,
            allowDuplicates: false,
            ...options
        };
        this.tags = [];
        this.init();
    }
    
    init() {
        this.element.innerHTML = `
            <div class="tag-input">
                <div class="tags-container"></div>
                <input type="text" class="tag-input-field" placeholder="${this.options.placeholder}">
            </div>
        `;
        
        this.tagsContainer = this.element.querySelector('.tags-container');
        this.inputField = this.element.querySelector('.tag-input-field');
        
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.addTag(this.inputField.value.trim());
                this.inputField.value = '';
            }
        });
    }
    
    addTag(tag) {
        if (!tag || this.tags.length >= this.options.maxTags) return;
        if (!this.options.allowDuplicates && this.tags.includes(tag)) return;
        
        this.tags.push(tag);
        this.renderTags();
        this.dispatchEvent('tagAdded', { tag });
    }
    
    removeTag(tag) {
        const index = this.tags.indexOf(tag);
        if (index > -1) {
            this.tags.splice(index, 1);
            this.renderTags();
            this.dispatchEvent('tagRemoved', { tag });
        }
    }
    
    renderTags() {
        this.tagsContainer.innerHTML = this.tags.map(tag => `
            <span class="tag-item">
                ${tag}
                <button type="button" class="remove-tag" data-tag="${tag}">×</button>
            </span>
        `).join('');
        
        // Add event listeners to remove buttons
        this.tagsContainer.querySelectorAll('.remove-tag').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.removeTag(e.target.dataset.tag);
            });
        });
    }
    
    getTags() {
        return [...this.tags];
    }
    
    setTags(tags) {
        this.tags = [...tags];
        this.renderTags();
    }
    
    dispatchEvent(eventName, detail) {
        this.element.dispatchEvent(new CustomEvent(eventName, { detail }));
    }
}

// Global Functions (for backward compatibility and convenience)
function showSuccess(message, duration = 5000) {
    UIUtils.showAlert(message, 'success', duration);
}

function showError(message, duration = 8000) {
    UIUtils.showAlert(message, 'danger', duration);
}

function showWarning(message, duration = 6000) {
    UIUtils.showAlert(message, 'warning', duration);
}

function showInfo(message, duration = 5000) {
    UIUtils.showAlert(message, 'info', duration);
}

// Authentication Management
class AuthManager {
    static async login(credentials) {
        try {
            const response = await AgentStudioAPI.post('/auth/login', credentials);
            const { token, user } = response.data;
            
            AgentStudioAPI.setAuthToken(token, credentials.remember);
            this.setCurrentUser(user);
            
            return { success: true, user };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    static async logout() {
        try {
            await AgentStudioAPI.post('/auth/logout');
        } catch (error) {
            console.warn('Logout request failed:', error);
        } finally {
            AgentStudioAPI.clearAuthToken();
            this.clearCurrentUser();
            window.location.href = '/login';
        }
    }
    
    static getCurrentUser() {
        const userStr = localStorage.getItem('agent_studio_user') || sessionStorage.getItem('agent_studio_user');
        return userStr ? JSON.parse(userStr) : null;
    }
    
    static setCurrentUser(user) {
        const userStr = JSON.stringify(user);
        if (AgentStudioAPI.getAuthToken() === localStorage.getItem('agent_studio_token')) {
            localStorage.setItem('agent_studio_user', userStr);
        } else {
            sessionStorage.setItem('agent_studio_user', userStr);
        }
        
        // Update UI
        this.updateUserUI(user);
    }
    
    static clearCurrentUser() {
        localStorage.removeItem('agent_studio_user');
        sessionStorage.removeItem('agent_studio_user');
    }
    
    static updateUserUI(user) {
        const usernameEl = document.getElementById('username');
        if (usernameEl && user) {
            usernameEl.textContent = user.name || user.email || 'User';
        }
    }
    
    static isAuthenticated() {
        return !!AgentStudioAPI.getAuthToken();
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize authentication state
    const currentUser = AuthManager.getCurrentUser();
    if (currentUser) {
        AuthManager.updateUserUI(currentUser);
    }
    
    // Set up global error handling
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        if (event.reason instanceof APIError && event.reason.status === 401) {
            showError('Your session has expired. Please log in again.');
            setTimeout(() => {
                AuthManager.logout();
            }, 2000);
        }
    });
    
    // Set up navigation active states
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Debug mode
    if (AgentStudioConfig.debug) {
        console.log('Agent Studio initialized in debug mode');
        window.AgentStudioAPI = AgentStudioAPI;
        window.UIUtils = UIUtils;
        window.AuthManager = AuthManager;
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AgentStudioAPI,
        UIUtils,
        AuthManager,
        TagInput,
        APIError
    };
}
