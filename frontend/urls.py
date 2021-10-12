from . import views
from django.urls import path


urlpatterns = [

    # ================================
    # Create Accounts and Logins Paths
    # ================================

    # For Admins

    # Create Account (Company) Forum
    path('create-account', views.create_account),
    # Create Account (Company) Process Forum
    path('create-account/process', views.process_create_account),

    # Create Account (Admin) Forum
    path('create-account/admin', views.create_account_admin),
    # Create Account (Admin) Process Forum
    path('create-account/admin/process', views.process_create_account_admin),

    # Sign In Admin Forum View
    path('signin-company-admin', views.signin_admin),
    # Sign In Admin Process Forum
    path('process-signin-admin', views.process_signin_admin),
    
    # For Employees 

    # Sign In Location Forum View
    path('', views.signin_location),
    # Sign In Location Process Forum
    path('process-signin-location', views.process_signin_location),

    # ==============================
    # ==== Location Paths ====
    # ==============================

    # ==== Location Views ====
    path('dashboard', views.dashboard),
    # Process Clock System
    path('process-clock', views.process_clock),

    # Process Delete Clock In/Out
    path('process-delete-clocksys/<int:clockSys_id>', views.process_remove_clocksys),

    path('admin-clock-view', views.admin_clock_view),
    
    path('logout', views.logout),


    # ==============================
    # ==== ADMIN Paths ====
    # ==============================

    # Admin Manager View
    path('manage/admin', views.manage_admin),

    # Create Admin Forum View
    path('manage/admin/create', views.create_new_account_admin),

    # Create Admin Process Forum
    path('manage/admin/create_new/process', views.process_create_new_account_admin),

    # Edit Admin Forum View
    path(f'manage/admin/edit/<int:admin_id>', views.manage_admin_edit),

    # Edit Admin Process Forum
    path(f'manage/admin/edit/<int:admin_id>/process', views.process_admin_edit),

    # Delete Admin Process 
    path(f'manage/admin/edit/<int:admin_id>/process/delete', views.process_admin_delete),

    # =========================
    # Company Manager Forum View
    # =========================

    path('manage/company', views.manage_company),

    # Edit Company Process Forum
    path('manage/company/edit', views.process_edit_company), 

    # Delete Company Process
    path('manage/admin/edit/process/delete', views.process_company_delete),


    # =====================
    # Location Manager View
    # =====================

    # Location Manage View
    path('manage/locations', views.manage_locations),

    # Create Locations Forum View
    path('manage/locations/create', views.manage_location_create),

    # Create locations Process Forum
    path('manage/locations/create/process', views.process_create_location),

    # Edit Locations Forum View 
    path(f'manage/locations/<int:location_id>/edit', views.manage_edit_location),

    # Edit Locations Process Forum
    path(f'manage/locations/<int:location_id>/edit/process', views.process_edit_locations),

    # Delete Locations Process
    path(f'manage/locations/edit/<int:location_id>/process/delete', views.process_delete_location),
    
    # ======================
    # Employee Manager View
    # ======================

    # Employee Manage View
    path('manage/employees', views.manage_employees),

    # Create Employee Forum
    path('manage/employees/create', views.manage_employees_create),

    # Create Employee Process Forum
    path('manage/employees/create/process', views.process_create_employee),

    # Edit Employee Forum View
    path('manage/employees/<int:employee_id>/edit', views.manage_edit_employees), 

    # Edit Employee Process Forum
    path('manage/employees/<int:employee_id>/edit/process', views.process_edit_employees),

    # Delete Employee
    path('manage/employees/<int:employee_id>/process/delete', views.process_delete_employee),


    # ======================
    # Settings Manager View
    # ======================
    path('settings', views.settings),

    # ==========
    # ETS Views 
    # ==========
    path('about', views.about)
]
