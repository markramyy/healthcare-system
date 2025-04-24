# API Overview

## Introduction
The Healthcare Management System API provides a RESTful interface for interacting with the system's core services. This API enables integration with external systems, mobile applications, and third-party services.

## API Versioning
The API follows semantic versioning (SemVer) and is currently at version 1.0.0. The version is included in the URL path:
```
https://api.healthcare-system.com/v1
```

## Base URL
All API endpoints are relative to the base URL:
```
https://api.healthcare-system.com/v1
```

## Response Format
All API responses are returned in JSON format with the following structure:
```json
{
    "status": "success|error",
    "data": {
        // Response data
    },
    "message": "Optional message",
    "errors": [] // Only present when status is "error"
}
```

## HTTP Methods
The API supports the following HTTP methods:
- `GET`: Retrieve resources
- `POST`: Create new resources
- `PUT`: Update existing resources
- `DELETE`: Remove resources
- `PATCH`: Partial updates to resources

## Rate Limiting
API requests are rate-limited to prevent abuse. The current limits are:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of requests:
- 2xx: Success
- 4xx: Client errors
- 5xx: Server errors

Detailed error messages are provided in the response body when errors occur.

## Authentication
All API endpoints require authentication except for public endpoints. See the [Authentication Documentation](authentication.md) for details on how to authenticate your requests.

## Available Endpoints
The API provides endpoints for the following core services:
- Patient Management
- Electronic Health Records (EHR)
- Appointment Scheduling
- Billing Management

For detailed information about specific endpoints, please refer to the [Endpoints Documentation](endpoints.md).

## Best Practices
1. Always include the `Accept` header with value `application/json`
2. Use HTTPS for all API requests
3. Implement proper error handling
4. Cache responses when appropriate
5. Follow the rate limiting guidelines

## Support
For API support or questions, please contact the API support team at api-support@healthcare-system.com.