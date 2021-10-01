from . import views
from django.urls import path


urlpatterns = [
    # All Employees
    path('all-employees', views.employee_filter_view),
    path('all-employees/process', views.process_all_employees_report),
    path('all-employees/process/totals/print', views.process_employees_all_totals_print),
    path('all-employees/process/records/print', views.process_employees_all__records_print),
    
    # Single Employee
    path(f'employees/<int:employee_id>', views.employee_report),
    path(f'employees/<int:employee_id>/process', views.process_employee_report),
    path(f'employees/<int:employee_id>/process/print', views.process_employee_report_print),
    
    # Locations
    path(f'locations/<int:location_id>', views.single_location_report),
    path(f'locations/<int:location_id>/process', views.process_single_location_report),
    path(f'locations/<int:location_id>/process/totals/print', views.process_location_totals_print),
    path(f'locations/<int:location_id>/process/records/print', views.process_location_records_print),

    # Edit/Delete
    path(f'employee/clockin/<int:clockin_id>/edit/', views.edit_report),
    path(f'employee/clockin/<int:clockin_id>/edit/process', views.process_edit_report),
    path('clockins/delete/process', views.process_delete_report)

]
