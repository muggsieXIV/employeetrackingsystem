from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Admin 
from company.models import Company, Location
from employees.models import Employee
from reports.models import ClockSystem
import datetime
import bcrypt
import pytz

# =================
# Create an Account
# =================

# Create Account (Company) Forum View
def create_account(request):
    return render(request, 'create-account.html')

# Create Account (Company) Process Forum
def process_create_account(request):
    if request.method != "POST":
        return redirect('/create-account')

    errors = Company.objects.company_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/create-account')

    company = Company.objects.create(
        name=request.POST['name'],
        image=request.POST['image']
    )
    request.session['company_id'] = company.id 
    return redirect('/create-account/admin')

# Create (Company) Administrator Forum View
def create_account_admin(request):
    context = {
        'company': Company.objects.get(id=request.session['company_id']),
        'company_name': ""
    }
    
    company_name = context['company'].name
    print(company_name)
    context['company_name'] = company_name

    return render(request, 'create-user.html', context)

# Create (Company) Administrator Process Forum
def process_create_account_admin(request):
    if request.method != "POST":
        return redirect('/create-account/admin')

    if 'company_id' not in request.session:
        return redirect('/create-account')

    errors = Admin.objects.admin_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/create-account/admin')

    print(request.session['company_id'])
    company_id=request.session['company_id']

    check_admin = Admin.objects.filter(email=request.POST['email'])

    if check_admin:
        messages.error(request, "Email already in use. Sign into your account or recover your password")
        return redirect('/create-account/admin')

    this_company = Company.objects.get(id=company_id)
    company_name = this_company.name
    request.session['company_name'] = company_name

    # hash password with Bcrypt - need to import above
    raw_pw = request.POST['password']
    hashed_pw = bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()

    admin = Admin.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
        company=this_company
    )

    request.session['admin_id'] = admin.id

    print(admin.last_name + ', ' + admin.first_name)

    request.session.flush()
    return redirect('/signin-company-admin')


# ========
# Sign In
# ========

# Sign in for Company Admin Forum View
def signin_admin(request):
    if 'admin_id' in request.session:
        return redirect('/manage/company')
    return render(request, 'admin-sign-in.html')

# Sign in for Company Admin Process Forum
def process_signin_admin(request):
    # will log in the company Admin
    # first check if receiving a POST request
    # if not a POST request:
    if request.method != "POST":
        return redirect('/signin-company-admin')

    # if a valid POST request, check for errors
    else:
        # check if login object is valid
        # import list of errors found
        errors = Admin.objects.login_validator(request.POST)

        # add the error messages to each error if any errors found in the
        # errors list - checks if list is empty or not - uses python message
        # library - need to import at the top
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)  # value is the error message string created in models.py
            return redirect('/signin-company-admin')

        # check if email is already in the database
        admin = Admin.objects.filter(email=request.POST['email'])

        if len(admin) == 0:  # if user does NOT exist
            messages.error(request, "Invalid email address or password!", extra_tags='login')
            return redirect('/signin-company-admin')

        # at this point, all checks pass and we can now unhash the password
        # unhash password with Bcrypt - need to import above
        login_raw_pw = request.POST['password']

        # checks if the entered password does not match the one in the database
        if not bcrypt.checkpw(login_raw_pw.encode(), admin[0].password.encode()):
            messages.error(request, "Invalid email address or password!", extra_tags='login')
            return redirect('/signin-company-admin')

        # place the user ID into session - set to the last user created:
        admin = Admin.objects.get(email=request.POST['email'])
        request.session['admin_id'] = admin.id
        company = Company.objects.get(admins=admin.id)
        request.session['company_id'] = company.id
        

        return redirect('/manage/company')

# Sign In for Employees (By location) Forum View
def signin_location(request):
    if 'location_id' in request.session:
        return redirect('/dashboard')

    return render(request, 'location-sign-in.html')

# Signin for Employees (By Location) Process Forum
def process_signin_location(request):
    if 'location_id' in request.session:
        return redirect('/dashboard')

    errors = Location.objects.login_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/', messages)
    
    location = Location.objects.get(username=request.POST['username'])
    print(location)

    if not location:  # if user does NOT exist
            messages.error(request, "Invalid username, try again!", extra_tags='username')
            return redirect('/')

    # at this point, all checks pass and we can now unhash the password
    # unhash password with Bcrypt - need to import above
    login_raw_pw = request.POST['password']

    # checks if the entered password does not match the one in the database
    if not bcrypt.checkpw(login_raw_pw.encode(), location.password.encode()):
        messages.error(request, "Invalid password, try again!", extra_tags='password')
        return redirect('/')

    # place the user ID into session - set to the last user created:
    request.session['location_id'] = location.id

    return redirect('/dashboard')

# ==============
# Employee Views
# ==============

# Employee Dashboard View For Logged into Location
def dashboard(request):
    # If user not logged in
    if 'location_id' not in request.session:
        return redirect('/')

    company = Company.objects.get(location=request.session['location_id'])
    # check active_employees in session is current
    context = {
        'all_employees': Employee.objects.filter(company=company.id),
        'company': company,
        'location': Location.objects.get(id=request.session['location_id'])
    }

    return render(request, 'clock.html', context) 

# Employee Process Clock In/Out
def process_clock(request):
    if 'location_id' not in request.session:
        return redirect('/')

    errors = ClockSystem.objects.clockin_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            message.errors(request, message)
        return redirect('/dashboard')

    if 'employee' not in request.POST:
        messages.error(request, 'Must choose an employee!')
        return redirect('/dashboard')

    location = Location.objects.get(id=request.session['location_id'])

    # Define the Employee
    e = Employee.objects.get(id=request.POST['employee'])

    now = datetime.datetime.now(pytz.timezone('US/Central'))

    # ===============
    # If Clocking In
    # ===============
    if request.POST['clocksys'] == "clockin":
        if e.is_active == True:
            messages.error(request, 'failed: ' + e.last_name + ', ' + e.first_name  + ' is already clocked in')
            return redirect('/dashboard')
        ClockSystem.objects.create(
            employee=e,
            location=location, 
            role=e.role,
            in_comment=request.POST['comment'], 
            date_in=now.strftime("%Y-%m-%d"),
            clocked_in_at=now.strftime("%H:%M:%S")
        )
        e.is_active = True

        e.save()

        success_msg = e.last_name + ', ' + e.first_name + ' successfully signed in at ' + str(now.strftime("%I:%M:%S%p"))
        messages.error(request, success_msg, extra_tags='success')


        return redirect('/dashboard')

    # ===============
    # if clocking out
    # ===============
    if request.POST['clocksys'] == 'clockout':
        # Check to make sure the employee is clocked in, and has not clocked out
        if e.is_active != True:
            messages.error(request, 'Failed: Employee ' + e.last_name + ', ' + e.first_name + ' is not clocked in.')
            return redirect('/dashboard')
        # If employee was clocked in: 
        if e.is_active == True:
            # Get the employee's last clockin
            cs = ClockSystem.objects.filter(location=request.session['location_id'])
            e_cs = cs.filter(employee=request.POST['employee'])
            last_login = e_cs[0]
            for clockins in e_cs:
                if clockins.id > last_login.id:
                    last_login = clockins

            # Calculate hours_worked
            last_login.clocked_out_at = now.strftime("%H:%M:%S")
            c_in = last_login.clocked_in_at
            c_out = last_login.clocked_out_at
            d_in = last_login.date_in
            d_out = now.strftime("%Y-%m-%d")

            datetime1_str = str(d_in) + ' ' + str(c_in)
            datetime2_str = str(d_out) + ' ' + str(c_out)
            
            datetime1_str = str(d_in) + ' ' + str(c_in)
            datetime2_str = str(d_out) + ' ' + str(c_out)

            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            diff = datetime.datetime.strptime(datetime2_str, datetimeFormat) - datetime.datetime.strptime(datetime1_str, datetimeFormat)

            # Setting Time Worked
            last_login.time_worked = str(diff)

            # Setting Comment
            last_login.out_comment = request.POST['comment']
            
            # Setting Date Out
            last_login.date_out = d_out
            
            # Set employe to inactive
            e.is_active = False

            last_login.save()

            e.save()

            success_msg = e.last_name + ', ' + e.first_name + ' successfully signed out at ' + str(now.strftime("%I:%M:%S%p"))
            messages.error(request, success_msg, extra_tags='success')

            return redirect('/dashboard')
            
    else:
        messages.error(request, 'Something went wrong. Please contact your admninistrator with code:303-B_FAIL')
        return(redirect('/dashboard'))

# Deletng clockSystem Data
def process_remove_clocksys(request, clockSys_id):
    if 'user_id' not in request.session:
        return redirect('/')
    clocksys_to_delete = ClockSystem.objects.get(id=clockSys_id)
    clocksys_to_delete.delete()
    return redirect('/dashboard')

def signout_location(request):
    request.session.flush()
    return redirect('/')

# =========================
# ADMIN VIEWS and FUNCTIONS
# =========================

# Manage Admin View
def manage_admin(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])
    
    context = {
        'admin': Admin.objects.get(id=request.session['admin_id']),
        'all_admins': Admin.objects.filter(company=request.session['company_id']),
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }
    

    return render(request, 'manage-admins.html', context)

# Create Admin Forum View
def create_new_account_admin(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'admin': Admin.objects.get(id=request.session['admin_id']),
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'manage-admin-create.html', context)

# Create Admin Process Forum
def process_create_new_account_admin(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    errors = Admin.objects.admin_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/manage/admin/edit/{{ this_admin.id }}', messages)
    

    this_company = Company.objects.get(admins=request.session['admin_id'])

    # hash password with Bcrypt - need to import above
    raw_pw = request.POST['password']
    hashed_pw = bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()

    Admin.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
        company=this_company
    )

    return redirect('/manage/admin')

# Manage Admin Forum View
def manage_admin_edit(request, admin_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'this_admin': Admin.objects.get(id=admin_id),
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'edit-admin.html', context)

# Edit Admin Process Forum
def process_admin_edit(request, admin_id):
    # If user not logged in
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    print(admin_id)
    this_admin = Admin.objects.get(id=admin_id)

    errors = Admin.objects.admin_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/manage/admin/edit/{{ this_admin.id }}', messages)
    
    # hash password with Bcrypt - need to import above
    raw_pw = request.POST['password']
    hashed_pw = bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()

    this_admin.first_name = request.POST['first_name']
    this_admin.last_name = request.POST['last_name']
    this_admin.email = request.POST['email']
    this_admin.password = hashed_pw
    this_admin.save()

    return redirect('/manage/admin', messages)

# Delete Admin Process
def process_admin_delete(request, admin_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    admin_to_delete = Admin.objects.get(id=admin_id)
    admin = request.session['admin_id']
    print(admin_to_delete.id)
    print(admin)

    errors = Admin.objects.delete_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/manage/admin/edit/{{ this_admin.id }}', messages)
    
    if admin_to_delete.id == admin:
        messages.error(request, "You cannot delete the Admin you are signed in with Please sign into another Admin account so you do not loose account access.") 
        return redirect(f'/manage/admin/edit/{admin_to_delete.id}')

    admin_to_delete.delete()
    return redirect('/manage/admin')

# ===========================
# COMPANY VIEWS and FUNCTIONS
# ===========================
# Edit Company Forum View
def manage_company(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'admin': Admin.objects.get(id=request.session['admin_id']),
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'manage-company.html', context)

# Edit Company Process Forum
def process_edit_company(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    errors = Company.objects.company_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/manage/company')

    if not request.POST['image'] and not request.POST['name']:
        return redirect('/manage/company')

    if not request.POST['name']:
        company.name = company.name
        company.image = request.POST['image']
        company.save()
        return redirect('/manage/company')

    if not request.POST['image']:
        company.name = request.POST['name']
        company.image = company.image
        company.save()
        return redirect('/manage/company')

    if request.POST['name'] and request.POST['image']:
        company.name = request.POST['name']
        company.image = request.POST['image']
        company.save()
        return redirect('/manage/company')


# Delete Company Process
def process_company_delete(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    company_to_delete = Company.objects.get(admins=request.session['admin_id'])

    company_to_delete.delete()
    request.session.flush()
    return redirect('/signin-company-admin')

# ============================
# LOCATION VIEWS and FUNCTIONS
# ============================
# Manage Locations View
def manage_locations(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company)
    }

    return render(request, 'manage-locations.html', context)

# Edit Locations Forum View
def manage_edit_location(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'location': Location.objects.get(id=location_id),
        'locations': Location.objects.filter(company=company)
    }

    return render(request, 'edit-location.html', context)

# Edit Locations Process Forum
def process_edit_locations(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    errors = Location.objects.location_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/create-account/admin/locations')

    location = Location.objects.get(id=location_id)
    company = Company.objects.get(admins=request.session['admin_id'])

    # hash password with Bcrypt - need to import above
    raw_pw = request.POST['password']
    hashed_pw = bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()

    location.name = request.POST['name']
    location.address = request.POST['address']
    location.city = request.POST['city']
    location.state = request.POST['state']
    location.country = request.POST['country']
    location.username = request.POST['username']
    location.password = hashed_pw
    location.company = company

    location.save()

    return redirect('/manage/locations')

# Create Location Forum View
def manage_location_create(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'manage-location-create.html', context)

# Create Location Process Forum
def process_create_location(request):
    if 'admin_id' not in request.session:
        return redirect('/create-account/admin/location')

    errors = Location.objects.location_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/create-account/admin/locations')
    
    this_company = Company.objects.get(admins=request.session['admin_id'])

    Location.objects.create(
        name=request.POST['name'],
        address=request.POST['address'],
        city=request.POST['city'],
        state=request.POST['state'],
        country=request.POST['country'],
        username=request.POST['username'],
        password=request.POST['password'],
        company=this_company
    )

    return redirect('/manage/locations')

# Delete Location Process
def process_delete_location(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    location = Location.objects.get(id=location_id)

    location.delete()

    return redirect('/manage/locations')

# ======================
# Manage Employees View
# ======================
def manage_employees(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'all_employees': Employee.objects.filter(company=company.id),
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'manage-employees.html', context)

# Create Employees Forum View
def manage_employees_create(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'create-employee.html', context)

# Create Employees Process Forum
def process_create_employee(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    errors = Employee.objects.employee_validator(request.POST)
    if len(errors) > 0:
        for message in errors.values():
            messages.error(request, message)
        return redirect('/create-account/admin/locations/employees')

    this_company = Company.objects.get(id=request.session['company_id'])

    Employee.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        role=request.POST['role'],
        is_active=False,
        company=this_company
    ) 

    return redirect('/manage/employees')

# Edit Employee Forum View
def manage_edit_employees(request, employee_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'employee': Employee.objects.get(id=employee_id),
        'locations': Location.objects.filter(company=company.id)
    }

    return render(request, 'edit-employee.html', context)

# Edit Employee Process Forum
def process_edit_employees(request, employee_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    employee = Employee.objects.get(id=employee_id)

    employee.first_name = request.POST['first_name']
    employee.last_name = request.POST['last_name']
    employee.role = request.POST['role']
    employee.company = company

    employee.save() 
    
    return redirect('/manage/employees')

# Delete Employee Process
def process_delete_employee(request, employee_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect('/manage/employees')

# Admin Clock View
def admin_clock_view(request):
    pass

# Admin Settings
def settings(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company, 
        'locations': Location.objects.filter(company=company.id)
    }
    return render(request, 'settings.html', context)

# =======
# Logout
# =======
# (Works Globally)
def logout(request):
    request.session.flush()
    return redirect('/')
