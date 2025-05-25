# Role-Based Access Control Documentation

## Overview
The healthcare system implements a role-based access control (RBAC) system to manage user permissions and access to different features based on their user type. This document outlines the available roles and their corresponding permissions.

<div style="page-break-after: always;"></div>

## Available Roles
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

## Detailed Access Control Matrix

### Patient Profile Management
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Profiles | ✓ | ✓ | Own patients | ✗ |
| View Profile | ✓ | ✓ | Own patients | Own only |
| Create Profile | ✓ | ✓ | ✗ | ✗ |
| Update Profile | ✓ | ✓ | Own patients | Own only |
| Delete Profile | ✓ | ✗ | ✗ | ✗ |

### Insurance Management
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Insurance | ✓ | ✓ | Own patients | Own only |
| View Insurance | ✓ | ✓ | Own patients | Own only |
| Create Insurance | ✓ | ✓ | ✗ | Own only |
| Update Insurance | ✓ | ✓ | ✗ | Own only |
| Delete Insurance | ✓ | ✗ | ✗ | Own only |

### Emergency Contact Management
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Contacts | ✓ | ✓ | Own patients | Own only |
| View Contact | ✓ | ✓ | Own patients | Own only |
| Create Contact | ✓ | ✓ | ✗ | Own only |
| Update Contact | ✓ | ✓ | ✗ | Own only |
| Delete Contact | ✓ | ✓ | ✗ | Own only |

### Appointment Management
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Appointments | ✓ | ✓ | Own | Own only |
| View Appointment | ✓ | ✓ | Own | Own only |
| Create Appointment | ✓ | ✓ | Own | Own only |
| Update Appointment | ✓ | ✓ | Own | Own only |
| Delete Appointment | ✓ | ✓ | Own | Own only |

### Medical Records
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Records | ✓ | ✓ | Own patients | Own only |
| View Record | ✓ | ✓ | Own patients | Own only |
| Create Record | ✓ | ✓ | Own patients | ✗ |
| Update Record | ✓ | ✓ | Own patients | ✗ |
| Delete Record | ✓ | ✓ | Own patients | ✗ |

### Billing Management
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Invoices | ✓ | ✓ | Own patients | Own only |
| View Invoice | ✓ | ✓ | Own patients | Own only |
| Create Invoice | ✓ | ✓ | ✗ | Own only |
| Update Invoice | ✓ | ✓ | ✗ | Own only |
| Delete Invoice | ✓ | ✓ | ✗ | Own only |

### Insurance Claims
| Action | Admin | Staff | Doctor | Patient |
|--------|-------|-------|--------|---------|
| List Claims | ✓ | ✓ | Own patients | Own only |
| View Claim | ✓ | ✓ | Own patients | Own only |
| Create Claim | ✓ | ✓ | ✗ | Own only |
| Update Claim | ✓ | ✓ | ✗ | Own only |
| Delete Claim | ✓ | ✓ | ✗ | Own only |

<div style="page-break-after: always;"></div>

## Implementation Details

### Permission Classes
The system uses custom permission classes for each viewset:

1. `PatientProfilePermission`
2. `InsurancePermission`
3. `EmergencyContactPermission`
4. `AppointmentTypePermission`
5. `AppointmentSlotPermission`
6. `AppointmentPermission`
7. `MedicalRecordPermission`
8. `DiagnosisPermission`
9. `TreatmentPermission`
10. `PrescriptionPermission`
11. `ServicePermission`
12. `InvoicePermission`
13. `InvoiceItemPermission`
14. `PaymentPermission`
15. `InsuranceClaimPermission`

### Key Features
1. **Object-Level Permissions**: Each permission class implements both view-level and object-level permissions
2. **Action-Based Access**: Different actions (list, retrieve, create, update, delete) have different permission requirements
3. **User Type Filtering**: Querysets are filtered based on user type
4. **Automatic Field Setting**: Certain fields are automatically set based on the user type

<div style="page-break-after: always;"></div>

## Security Considerations

1. All permissions are enforced at both the view and object level
2. Querysets are filtered to ensure users only see their authorized data
3. Create/update operations automatically set user-specific fields
4. Delete operations have additional restrictions for certain user types
5. All endpoints require authentication
6. Permissions are checked before any data access or modification

<div style="page-break-after: always;"></div>

## Testing Guidelines

1. Test each endpoint with different user types
2. Verify that users can only access their authorized data
3. Test create/update operations to ensure proper field setting
4. Verify that delete operations are properly restricted
5. Test edge cases and unauthorized access attempts
