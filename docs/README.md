# Healthcare Management System Documentation

## Overview
The Healthcare Management System is a comprehensive platform designed to streamline healthcare operations, manage patient records, and improve the overall healthcare delivery process. This documentation provides detailed information about each component of the system and how they work together.

## Table of Contents

1. [System Architecture](architecture.md)
   - Overview of the system's architecture
   - Component interactions
   - Data flow

2. [Core Services](services/README.md)
   - [Patient Management](services/patient_management.md)
   - [Electronic Health Records (EHR)](services/ehr.md)
   - [Appointment Scheduling](services/appointment.md)
   - [Billing Management](services/billing.md)

3. [Technical Infrastructure](infrastructure/README.md)
   - [Docker Containerization](infrastructure/docker.md)
   - [Kubernetes Orchestration](infrastructure/kubernetes.md)
   - [Monitoring and Logging](infrastructure/monitoring.md)
   - [Database Management](infrastructure/database.md)

4. [Security and Compliance](security/README.md)
   - [Authentication and Authorization](security/auth.md)
   - [Data Protection](security/data_protection.md)
   - [Compliance Standards](security/compliance.md)
   - [Role-Based Access Control](security/role_based_access.md)

5. [User Guides](user_guides/README.md)
   - [Admin Guide](user_guides/admin.md)
   - [Doctor Guide](user_guides/doctor.md)
   - [Staff Guide](user_guides/staff.md)
   - [Patient Guide](user_guides/patient.md)

6. [API Documentation](api/README.md)
   - [API Overview](api/overview.md)
   - [Authentication](api/authentication.md)
   - [Endpoints](api/endpoints.md)

7. [Deployment Guide](deployment/README.md)
   - [Development Setup](deployment/development.md)
   - [Production Deployment](deployment/production.md)
   - [Environment Configuration](deployment/environment.md)

<div style="page-break-after: always;"></div>

## Role-Based Access Control

The system implements a comprehensive role-based access control (RBAC) system to manage user permissions and access to different features. The following roles are available:

### Available Roles

1. **Admin** (`admin`)
   - Full system access
   - Can manage all users and settings
   - Can view and manage all records
   - Can perform all operations on all resources

2. **Staff** (`staff`)
   - Can view all records
   - Can manage appointments
   - Can handle billing and insurance
   - Limited delete permissions on certain resources

3. **Doctor** (`doctor`)
   - Can manage their own patients' records
   - Can create and manage their own appointments
   - Can view and manage their patients' medical records
   - Can create prescriptions and treatments for their patients
   - Can view their patients' billing information

4. **Patient** (`patient`)
   - Can view and manage their own profile
   - Can view and manage their own appointments
   - Can view their own medical records
   - Can view their own prescriptions and treatments
   - Can manage their own insurance and emergency contacts
   - Can view and manage their own billing information

<div style="page-break-after: always;"></div>

### Access Control Matrix

The system implements detailed access control matrices for various resources:

- Patient Profile Management
- Insurance Management
- Emergency Contact Management
- Appointment Management
- Medical Records
- Billing Management
- Insurance Claims

For detailed access control matrices and implementation details, please refer to the [Role-Based Access Control Documentation](role_based_access.md).

## Getting Started
To get started with the Healthcare Management System, please refer to the [Development Setup Guide](deployment/development.md) for local installation and the [User Guides](user_guides/README.md) for system usage.

## Support
For technical support or questions, please contact the system administrator or refer to the [Troubleshooting Guide](troubleshooting.md).