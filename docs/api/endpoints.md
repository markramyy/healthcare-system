# API Endpoints

## Overview
This document provides detailed information about all available API endpoints in the Healthcare Management System. Each endpoint is documented with its URL, method, parameters, and example responses.

## Base URL
All endpoints are relative to: `https://api.healthcare-system.com/v1`

## Common Parameters
- `page`: Page number for paginated results (default: 1)
- `limit`: Number of items per page (default: 20, max: 100)
- `sort`: Field to sort by (default: created_at)
- `order`: Sort order (asc/desc, default: desc)

<div style="page-break-after: always;"></div>

## Patient Management

### List Patients
```http
GET /patients
```

**Query Parameters:**
- `search`: Search term for patient name or ID
- `status`: Patient status filter
- `department`: Department filter

**Response:**
```json
{
    "status": "success",
    "data": {
        "patients": [
            {
                "id": "PAT123",
                "name": "John Doe",
                "date_of_birth": "1980-01-01",
                "gender": "male",
                "contact": {
                    "phone": "+1234567890",
                    "email": "john@example.com"
                },
                "status": "active"
            }
        ],
        "pagination": {
            "total": 100,
            "page": 1,
            "limit": 20
        }
    }
}
```

### Get Patient Details
```http
GET /patients/{patient_id}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": "PAT123",
        "name": "John Doe",
        "date_of_birth": "1980-01-01",
        "gender": "male",
        "contact": {
            "phone": "+1234567890",
            "email": "john@example.com"
        },
        "medical_history": [],
        "allergies": [],
        "current_medications": []
    }
}
```

<div style="page-break-after: always;"></div>

## Electronic Health Records (EHR)

### Create Medical Record
```http
POST /ehr/records
```

**Request Body:**
```json
{
    "patient_id": "PAT123",
    "visit_date": "2024-03-15",
    "doctor_id": "DOC456",
    "diagnosis": "Common cold",
    "prescription": "Rest and fluids",
    "notes": "Patient should return in 1 week if symptoms persist"
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "record_id": "EHR789",
        "created_at": "2024-03-15T10:30:00Z"
    }
}
```

### Get Patient Medical History
```http
GET /ehr/patients/{patient_id}/history
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "records": [
            {
                "record_id": "EHR789",
                "visit_date": "2024-03-15",
                "doctor": {
                    "id": "DOC456",
                    "name": "Dr. Smith"
                },
                "diagnosis": "Common cold",
                "prescription": "Rest and fluids"
            }
        ]
    }
}
```

<div style="page-break-after: always;"></div>

## Appointment Scheduling

### Create Appointment
```http
POST /appointments
```

**Request Body:**
```json
{
    "patient_id": "PAT123",
    "doctor_id": "DOC456",
    "date": "2024-03-20",
    "time": "14:30",
    "type": "checkup",
    "notes": "Regular checkup"
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "appointment_id": "APT123",
        "status": "scheduled",
        "created_at": "2024-03-15T11:00:00Z"
    }
}
```

### List Appointments
```http
GET /appointments
```

**Query Parameters:**
- `patient_id`: Filter by patient
- `doctor_id`: Filter by doctor
- `date`: Filter by date
- `status`: Filter by status

**Response:**
```json
{
    "status": "success",
    "data": {
        "appointments": [
            {
                "id": "APT123",
                "patient": {
                    "id": "PAT123",
                    "name": "John Doe"
                },
                "doctor": {
                    "id": "DOC456",
                    "name": "Dr. Smith"
                },
                "date": "2024-03-20",
                "time": "14:30",
                "type": "checkup",
                "status": "scheduled"
            }
        ]
    }
}
```

<div style="page-break-after: always;"></div>

## Billing Management

### Create Invoice
```http
POST /billing/invoices
```

**Request Body:**
```json
{
    "patient_id": "PAT123",
    "appointment_id": "APT123",
    "items": [
        {
            "description": "Consultation",
            "amount": 100.00
        },
        {
            "description": "Medication",
            "amount": 50.00
        }
    ]
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "invoice_id": "INV123",
        "total_amount": 150.00,
        "status": "pending",
        "due_date": "2024-04-15"
    }
}
```

### Get Patient Billing History
```http
GET /billing/patients/{patient_id}/history
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "invoices": [
            {
                "id": "INV123",
                "date": "2024-03-15",
                "total_amount": 150.00,
                "status": "paid",
                "items": [
                    {
                        "description": "Consultation",
                        "amount": 100.00
                    },
                    {
                        "description": "Medication",
                        "amount": 50.00
                    }
                ]
            }
        ]
    }
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "status": "error",
    "message": "Invalid request parameters",
    "errors": [
        {
            "field": "date",
            "message": "Invalid date format"
        }
    ]
}
```

### 401 Unauthorized
```json
{
    "status": "error",
    "message": "Authentication required",
    "errors": []
}
```

### 403 Forbidden
```json
{
    "status": "error",
    "message": "Insufficient permissions",
    "errors": []
}
```

### 404 Not Found
```json
{
    "status": "error",
    "message": "Resource not found",
    "errors": []
}
```

### 429 Too Many Requests
```json
{
    "status": "error",
    "message": "Rate limit exceeded",
    "errors": []
}
```

### 500 Internal Server Error
```json
{
    "status": "error",
    "message": "Internal server error",
    "errors": []
}
```