# API Authentication

## Overview
The Healthcare Management System API uses OAuth 2.0 with JWT (JSON Web Tokens) for authentication. This provides a secure and standardized way to authenticate API requests.

## Authentication Methods

### 1. OAuth 2.0
The API supports the following OAuth 2.0 flows:
- Authorization Code Flow
- Client Credentials Flow
- Password Grant Flow

### 2. JWT Authentication
For direct API access, JWT tokens are used. These tokens are obtained through the OAuth 2.0 process.

## Getting Started

### 1. Register Your Application
To use the API, you must first register your application:
1. Contact the API support team
2. Provide your application details
3. Receive your client credentials (Client ID and Client Secret)

### 2. Obtaining Access Tokens

#### Authorization Code Flow
```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=AUTHORIZATION_CODE
&redirect_uri=REDIRECT_URI
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET
```

#### Client Credentials Flow
```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET
```

#### Password Grant Flow
```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=password
&username=USERNAME
&password=PASSWORD
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET
```

## Using Access Tokens

### Including Tokens in Requests
Include the access token in the Authorization header:
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Token Expiration
- Access tokens expire after 1 hour
- Refresh tokens expire after 30 days
- You should implement token refresh logic in your application

### Refreshing Tokens
```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token=REFRESH_TOKEN
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET
```

## Security Best Practices

1. **Token Storage**
   - Store tokens securely
   - Never expose tokens in client-side code
   - Use secure storage mechanisms

2. **Token Handling**
   - Implement token refresh logic
   - Handle token expiration gracefully
   - Validate tokens before use

3. **Request Security**
   - Always use HTTPS
   - Include proper headers
   - Validate all input

4. **Error Handling**
   - Handle authentication errors appropriately
   - Implement proper logging
   - Monitor for suspicious activity

## Common Authentication Errors

| Error Code | Description | Resolution |
|------------|-------------|------------|
| 401 | Unauthorized | Check token validity and expiration |
| 403 | Forbidden | Verify permissions and scope |
| 429 | Too Many Requests | Implement rate limiting |

## Support
For authentication-related issues or questions, please contact:
- API Support: api-support@healthcare-system.com
- Security Team: security@healthcare-system.com