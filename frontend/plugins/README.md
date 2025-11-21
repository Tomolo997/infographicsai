# Plugins

## CSRF Token Plugin

The `csrf.js` plugin automatically sets up CSRF token handling for the application. This plugin:

1. Runs on the client-side when the application initializes
2. Fetches a CSRF token from the backend API
3. Sets the token in the Axios headers for all subsequent API requests

### How it works

1. The plugin calls the `setupCSRF()` function from the API client when the application loads
2. The API client checks if a CSRF token is already set before making a request
3. If a 403 error occurs that might be related to CSRF token expiration, the token is automatically refreshed

### Benefits

- No need to manually call `setupCSRF()` before making API requests
- Automatic token refresh if the token expires
- Centralized CSRF token management

### Implementation Details

- The CSRF token is obtained from the Django backend via the `/infos/get-csrf/` endpoint
- The token is stored in the Axios default headers as `X-CSRFToken`
- The plugin is configured to run only on the client-side

### Related Files

- `frontend/plugins/csrf.js`: The plugin implementation
- `frontend/services/apiClient.js`: Contains the CSRF token setup and refresh logic
- `app/infos/views.py`: Contains the Django view that provides the CSRF token 