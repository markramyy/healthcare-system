# Role-Based Access Control Documentation

## Overview
The healthcare system implements a role-based access control (RBAC) system to manage user permissions and access to different features based on their user type. This document outlines the available roles and their corresponding permissions.

## Available Roles
1. **Admin** (`admin`)
   - Full system access
   - Can manage all users and settings
   - Can view and manage all records

2. **Doctor** (`doctor`)
   - Can manage patient records
   - Can create and manage appointments
   - Can view and manage medical records
   - Can create prescriptions and treatments

3. **Nurse** (`nurse`)
   - Can view patient records
   - Can manage appointments
   - Can update medical records
   - Can view prescriptions and treatments

4. **Staff** (`staff`)
   - Can manage appointments
   - Can handle billing and insurance
   - Can view basic patient information

5. **Patient** (`patient`)
   - Can view own records
   - Can manage own appointments
   - Can view own prescriptions and treatments

## Access Control Implementation

### Decorators
The system uses custom decorators to enforce role-based access control:

```python
from healthcare_ms.core.decorators import role_required

@role_required('admin')
def admin_only_view(request):
    # Only admins can access this view
    pass

@role_required('doctor', 'nurse')
def medical_staff_view(request):
    # Both doctors and nurses can access this view
    pass
```

### Available Decorators
1. `@admin_required` - Admin only
2. `@doctor_required` - Doctor only
3. `@nurse_required` - Nurse only
4. `@staff_required` - Staff only
5. `@patient_required` - Patient only
6. `@staff_or_admin_required` - Staff or Admin
7. `@doctor_or_nurse_required` - Doctor or Nurse
8. `@doctor_or_admin_required` - Doctor or Admin

## Feature Access Matrix

| Feature | Admin | Doctor | Nurse | Staff | Patient |
|---------|-------|--------|-------|-------|---------|
| User Management | ✓ | ✗ | ✗ | ✗ | ✗ |
| Patient Records | ✓ | ✓ | ✓ | ✗ | Own only |
| Medical Records | ✓ | ✓ | ✓ | ✗ | Own only |
| Appointments | ✓ | ✓ | ✓ | ✓ | Own only |
| Prescriptions | ✓ | ✓ | ✓ | ✗ | Own only |
| Treatments | ✓ | ✓ | ✓ | ✗ | Own only |
| Billing | ✓ | ✗ | ✗ | ✓ | Own only |
| Insurance | ✓ | ✗ | ✗ | ✓ | Own only |

## Implementation Guidelines

1. Always use the appropriate decorator for role-based access control
2. When creating new views, consider which roles should have access
3. Use the most restrictive access level possible
4. For combined role access, use the appropriate combined decorator
5. Test access control thoroughly for each role

## Example Usage

```python
from healthcare_ms.core.decorators import admin_required, doctor_required, staff_or_admin_required

@admin_required
def manage_users(request):
    # Only admins can manage users
    pass

@doctor_required
def create_prescription(request):
    # Only doctors can create prescriptions
    pass

@staff_or_admin_required
def manage_appointments(request):
    # Both staff and admins can manage appointments
    pass
```

## Security Considerations

1. Never rely solely on frontend checks for access control
2. Always implement server-side role verification
3. Use the decorators consistently across all views
4. Regularly audit access control implementations
5. Keep the documentation updated with any changes to access control
