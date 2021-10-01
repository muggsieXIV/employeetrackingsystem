
from django.shortcuts import render, redirect
from django.contrib import messages
from employees.models import Employee
from .models import ClockSystem
from company.models import Location, Company
import datetime, time
import pytz


# =================
# Location Reports
# =================

# Full Report for a Location
def single_location_report(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])
    location = Location.objects.get(id=location_id)

    context = {
        'company': company,
        'all_locations': location,
        'locations': Location.objects.filter(company=company.id), 
        'location': location,
        'all_employees': Employee.objects.filter(company=company.id),
        'res': [],
        'rec': [],
    }

    now = datetime.datetime.now()

    employees = context['all_employees']

    rec = context['rec']

    for employee in employees:
        qued = []
        
        first_qued = ClockSystem.objects.filter(employee=employee.id)
        for data in first_qued:
            if data.location == location:
                qued.append(data)
                rec.append(data)

        days_worked = str(len(qued))

        time_list = []
        for data in qued:
            if not data.date_out:
                time_out = now.strftime("%H:%M:%S")
                date_out = now.strftime("%Y-%m-%d")
                dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
                dt_2 = str(date_out) + ' ' + str(time_out)
                datetimeFormat = '%Y-%m-%d %H:%M:%S'
                diff = datetime.datetime.strptime(dt_2, datetimeFormat) - datetime.datetime.strptime(dt_1, datetimeFormat)
                time_list.append(str(diff))
            else:
                time_list.append(data.time_worked)
        
        total_secs = 0
        for tm in time_list:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs, sec = divmod(total_secs, 60)
        hr, min = divmod(total_secs, 60)
        total_time_worked = "%d:%02d:%02d" % (hr, min, sec)


        # Exporting Employee data to frontend
        employee_data = {
            'id': employee.id, 
            'last_name': employee.last_name, 
            'first_name': employee.first_name, 
            'days_worked': days_worked, 
            'is_active': employee.is_active,
            'total_time_worked': total_time_worked,
            'all_clock_ins': qued,
        }
        context['res'].append(employee_data)
    
    rec = []
    csy_qued = ClockSystem.objects.filter(location=location_id)
    for data in csy_qued:
        rec.append(data)
    rec.reverse()
    context['rec'] = rec

    return render(request, 'location-report.html', context)

# Location Report for Date Range
def process_single_location_report(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'location': Location.objects.get(id=location_id),
        'all_employees': Employee.objects.filter(company=company.id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'res': [],
        'rec': []
    }

    start_date = str(context['start_date'])
    end_date = str(context['end_date'])
    qued = []
    rec = []
    res = []
    
    # Getting All Location Records for Date Range 
    loc_rec = ClockSystem.objects.filter(location=location_id).order_by('created_at')

    for data in loc_rec:
        if data.location == context['location']:
            qued.append(data)

    # Setting the Records for start_date to end_date
    for data in qued:
        # setting string dates to datetime for evaluation
        s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        d_in = str(data.date_in)
        eval = datetime.datetime.strptime(d_in, "%Y-%m-%d")
        # evaluating our dates - if in range add to clock_ins
        if s <= eval:
            if eval <= e:
                rec.append(data)

    rec.reverse()
    context['rec'] = rec 

    # Generate employee totals
    for employee in context['all_employees']:

        employee_qued = []
        for data in rec:
            if data.employee == employee: 
                employee_qued.append(data)

        days_worked = str(len(employee_qued))

        # Getting Time Worked 
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        time_list = []
        for data in employee_qued:
            if not data.date_out:
                time_out = now.strftime("%H:%M:%S")
                date_out = now.strftime("%Y-%m-%d")
                dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
                dt_2 = str(date_out) + ' ' + str(time_out)
                dtf = '%Y-%m-%d %H:%M:%S'
                diff = datetime.datetime.strptime(dt_2, dtf) - datetime.datetime.strptime(dt_1, dtf)
                time_list.append(str(diff))
            else:
                time_list.append(data.time_worked)
        total_secs = 0
        for tm in time_list:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs, sec = divmod(total_secs, 60)
        hr, min = divmod(total_secs, 60)
        total_time_worked = "%d:%02d:%02d" % (hr, min, sec)
    
        employee_data = {
            'id': employee.id, 
            'last_name': employee.last_name, 
            'first_name': employee.first_name, 
            'is_active': employee.is_active,
            'days_worked': days_worked, 
            'total_time_worked': total_time_worked
        }

        res.append(employee_data)
    
    context['res'] = res 

    return render(request, 'report-location-date-range.html', context)

# Process Print Location Report for Date Range
def process_location_records_print(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'location': Location.objects.get(id=location_id),
        'all_employees': Employee.objects.filter(company=company.id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'res': [],
        'rec': []
    }

    start_date = str(context['start_date'])
    end_date = str(context['end_date'])
    qued = []
    rec = []
    res = []
    
    # Getting All Location Records for Date Range 
    loc_rec = ClockSystem.objects.filter(location=location_id).order_by('created_at')

    for data in loc_rec:
        if data.location == context['location']:
            qued.append(data)

    # Setting the Records for start_date to end_date
    for data in qued:
        # setting string dates to datetime for evaluation
        s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        d_in = str(data.date_in)
        eval = datetime.datetime.strptime(d_in, "%Y-%m-%d")

        # evaluating our dates - if in range add to clock_ins
        if s <= eval:
            if eval <= e:
                rec.append(data)
            
    rec.reverse()
    context['rec'] = rec 

    return render(request, 'report-location-all-records-print.html', context)

# Process Print Location report totals
def process_location_totals_print(request, location_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'location': Location.objects.get(id=location_id),
        'all_employees': Employee.objects.filter(company=company.id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'res': [],
        'rec': []
    }

    start_date = str(context['start_date'])
    end_date = str(context['end_date'])
    qued = []
    rec = []
    res = []
    
    # Getting All Location Records for Date Range 
    loc_rec = ClockSystem.objects.filter(location=location_id).order_by('created_at')

    for data in loc_rec:
        if data.location == context['location']:
            qued.append(data)

    # Setting the Records for start_date to end_date
    for data in qued:
        # setting string dates to datetime for evaluation
        s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        d_in = str(data.date_in)
        eval = datetime.datetime.strptime(d_in, "%Y-%m-%d")
        # evaluating our dates - if in range add to clock_ins
        if s <= eval:
            if eval <= e:
                rec.append(data)

    rec.reverse()
    context['rec'] = rec 

    # Generate employee totals
    for employee in context['all_employees']:

        employee_qued = []
        for data in rec:
            if data.employee == employee: 
                employee_qued.append(data)

        days_worked = str(len(employee_qued))

        # Getting Time Worked 
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        time_list = []
        for data in employee_qued:
            if not data.date_out:
                time_out = now.strftime("%H:%M:%S")
                date_out = now.strftime("%Y-%m-%d")
                dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
                dt_2 = str(date_out) + ' ' + str(time_out)
                dtf = '%Y-%m-%d %H:%M:%S'
                diff = datetime.datetime.strptime(dt_2, dtf) - datetime.datetime.strptime(dt_1, dtf)
                time_list.append(str(diff))
            else:
                time_list.append(data.time_worked)
        total_secs = 0
        for tm in time_list:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs, sec = divmod(total_secs, 60)
        hr, min = divmod(total_secs, 60)
        total_time_worked = "%d:%02d:%02d" % (hr, min, sec)
    
        employee_data = {
            'id': employee.id, 
            'last_name': employee.last_name, 
            'first_name': employee.first_name, 
            'is_active': employee.is_active,
            'days_worked': days_worked, 
            'total_time_worked': total_time_worked
        }

        res.append(employee_data)
    
    context['res'] = res 

    return render(request, 'report-location-all-totals-print.html', context)


# ==================
# Employees Reports
# ==================

# Report View for All Employees
# Page allows users to filter records for all employees or view individual employee reports
def employee_filter_view(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'all_employees': Employee.objects.filter(company=company.id),
        'company': company, 
        'locations': Location.objects.filter(company=company.id),
        'res': [],
    }

    print("Employee Reports")

    return render(request, 'filter-employees.html', context)

# Process All Employees Report
# Displays a report for all employees in company
def process_all_employees_report(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'all_employees': Employee.objects.filter(company=company.id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'all_clockins': [],
        'res': [],
        'rec': []
    }

    # Get the set start/end dates for Filtering Clockins
    start_date = str(context['start_date'])
    end_date = str(context['end_date'])
    rec = []

    # Parse through employees 
    all_employees = context['all_employees']
    for employee in all_employees:
        qued = []

        qued = ClockSystem.objects.filter(employee=employee.id)

        clock_ins = []
        for data in qued:
            # setting string dates to datetime for evaluation
            s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            d_in = str(data.date_in)
            eval = datetime.datetime.strptime(d_in, "%Y-%m-%d")

            # evaluating our dates - if in range add to clock_ins
            if s <= eval:
                if eval <= e:
                    clock_ins.append(data)
                    record = {
                        'is_flagged': data.is_flagged,
                        'employee': data.employee,
                        'date_in': data.date_in,
                        'time_in': data.clocked_in_at,
                        'time_out': data.clocked_out_at,
                        'time_worked': data.time_worked,
                        'in_comment': data.in_comment,
                        'out_comment': data.out_comment,
                        'location': data.location,
                        'role': data.role
                    }
                    rec.append(record)
        days_worked = str(len(clock_ins))
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        time_list = []
        # Getting Time Worked
        for data in clock_ins:
            if not data.date_out:
                time_out = now.strftime("%H:%M:%S")
                date_out = now.strftime("%Y-%m-%d")
                dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
                dt_2 = str(date_out) + ' ' + str(time_out)
                dtf = '%Y-%m-%d %H:%M:%S'
                diff = datetime.datetime.strptime(dt_2, dtf) - datetime.datetime.strptime(dt_1, dtf)
                time_list.append(str(diff))
            else:
                time_list.append(data.time_worked)
        total_secs = 0
        for tm in time_list:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs, sec = divmod(total_secs, 60)
        hr, min = divmod(total_secs, 60)
        total_time_worked = "%d:%02d:%02d" % (hr, min, sec)

        employee_data = {
            'id': employee.id, 
            'last_name': employee.last_name, 
            'first_name': employee.first_name, 
            'days_worked': days_worked, 
            'total_time_worked': total_time_worked
        }

        context['res'].append(employee_data) 
        context['rec'] = rec
        context['rec'].reverse



    return render(request, 'report-employees-all.html', context)

# Process All Employees Totals
# prints out all company employee totals for filtered date range
def process_employees_all_totals_print(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'all_employees': Employee.objects.filter(company=company.id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'all_clockins': [],
        'res': [],
        'rec': []
    }

    # Get the set start/end dates for Filtering Clockins
    start_date = str(context['start_date'])
    end_date = str(context['end_date'])
    rec = []

    # Parse through employees 
    all_employees = context['all_employees']
    for employee in all_employees:
        qued = []
        days_worked = ""
        qued = ClockSystem.objects.filter(employee=employee.id)

        clock_ins = []
        for data in qued:
            # setting string dates to datetime for evaluation
            s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            d_in = str(data.date_in)
            eval = datetime.datetime.strptime(d_in, "%Y-%m-%d")

            # evaluating our dates - if in range add to clock_ins
            if s <= eval:
                if eval <= e:
                    clock_ins.append(data)
                    record = {
                        'is_flagged': data.is_flagged,
                        'employee': data.employee,
                        'date_in': data.date_in,
                        'time_in': data.clocked_in_at,
                        'time_out': data.clocked_out_at,
                        'time_worked': data.time_worked,
                        'in_comment': data.in_comment,
                        'out_comment': data.out_comment,
                        'location': data.location,
                        'role': data.role,
                    }
                    rec.append(record)

        days_worked = str(len(clock_ins))
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        time_list = []
        # Getting Time Worked
        for data in clock_ins:
            if not data.date_out:
                time_out = now.strftime("%H:%M:%S")
                date_out = now.strftime("%Y-%m-%d")
                dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
                dt_2 = str(date_out) + ' ' + str(time_out)
                dtf = '%Y-%m-%d %H:%M:%S'
                diff = datetime.datetime.strptime(dt_2, dtf) - datetime.datetime.strptime(dt_1, dtf)
                time_list.append(str(diff))
            else:
                time_list.append(data.time_worked)
        total_secs = 0
        for tm in time_list:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs, sec = divmod(total_secs, 60)
        hr, min = divmod(total_secs, 60)
        total_time_worked = "%d:%02d:%02d" % (hr, min, sec)

        employee_data = {
            'id': employee.id, 
            'last_name': employee.last_name, 
            'first_name': employee.first_name, 
            'days_worked': days_worked, 
            'total_time_worked': total_time_worked
        }

        context['res'].append(employee_data) 
        context['rec'] = rec
        context['rec'].reverse

    return render(request, 'report-employees-all-totals-print.html', context)

# Print All Employees Records
# prints the report for all employees in company for filtered date range
def process_employees_all__records_print(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'all_employees': Employee.objects.filter(company=company.id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'all_clockins': [],
        'res': [],
        'rec': []
    }

    # Get the set start/end dates for Filtering Clockins
    start_date = str(context['start_date'])
    end_date = str(context['end_date'])
    rec = []

    # Parse through employees 
    all_employees = context['all_employees']
    for employee in all_employees:
        qued = []
        days_worked = ""
        qued = ClockSystem.objects.filter(employee=employee.id)

        clock_ins = []
        for data in qued:
            # setting string dates to datetime for evaluation
            s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            d_in = str(data.date_in)
            eval = datetime.datetime.strptime(d_in, "%Y-%m-%d")

            # evaluating our dates - if in range add to clock_ins
            if s <= eval:
                if eval <= e:
                    clock_ins.append(data)
                    record = {
                        'is_flagged': data.is_flagged,
                        'employee': data.employee,
                        'date_in': data.date_in,
                        'time_in': data.clocked_in_at,
                        'time_out': data.clocked_out_at,
                        'time_worked': data.time_worked,
                        'in_comment': data.in_comment,
                        'out_comment': data.out_comment,
                        'location': data.location,
                        'role': data.role,
                    }
                    rec.append(record)

        days_worked = str(len(clock_ins))
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        time_list = []
        # Getting Time Worked
        for data in clock_ins:
            if not data.date_out:
                time_out = now.strftime("%H:%M:%S")
                date_out = now.strftime("%Y-%m-%d")
                dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
                dt_2 = str(date_out) + ' ' + str(time_out)
                dtf = '%Y-%m-%d %H:%M:%S'
                diff = datetime.datetime.strptime(dt_2, dtf) - datetime.datetime.strptime(dt_1, dtf)
                time_list.append(str(diff))
            else:
                time_list.append(data.time_worked)
        total_secs = 0
        for tm in time_list:
            time_parts = [int(s) for s in tm.split(':')]
            total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
        total_secs, sec = divmod(total_secs, 60)
        hr, min = divmod(total_secs, 60)
        total_time_worked = "%d:%02d:%02d" % (hr, min, sec)

        employee_data = {
            'id': employee.id, 
            'last_name': employee.last_name, 
            'first_name': employee.first_name, 
            'days_worked': days_worked, 
            'total_time_worked': total_time_worked
        }

        context['res'].append(employee_data) 
        rec.reverse()
        context['rec'] = rec

    return render(request, 'report-employees-all-records-print.html', context)

# Report View For Single Employee
# displays all data for employee
def employee_report(request, employee_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'employee': Employee.objects.get(id=employee_id),
        'all_clockins': ClockSystem.objects.filter(employee=employee_id),
        'days_worked': "",
        'total_time_worked': "",
        'res': [],
        'rec': []
    }

    now = datetime.datetime.now(pytz.timezone('US/Central'))

    datetimeFormat = '%H:%M:%S'
    # Getting time_worked for employee
    timeList = []
    rec = []

    for data in context['all_clockins']:
        rec.append(data)

        if not data.date_out:
            time_out = now.strftime("%H:%M:%S")
            date_out = now.strftime("%Y-%m-%d")
            dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
            dt_2 = str(date_out) + ' ' + str(time_out)
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            diff = datetime.datetime.strptime(dt_2, datetimeFormat) - datetime.datetime.strptime(dt_1, datetimeFormat)
            timeList.append(str(diff))
        else:
            timeList.append(data.time_worked)
    # Adding time worked for employee
    total_secs = 0
    for tm in timeList:
        time_parts = [int(s) for s in tm.split(':')]
        total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
    total_secs, sec = divmod(total_secs, 60)
    hr, min = divmod(total_secs, 60)
    total_time_worked = "%d:%02d:%02d" % (hr, min, sec)
    context['total_time_worked'] = total_time_worked

    days_worked = str(len(context['all_clockins']))
    context['days_worked'] = days_worked


    print(context['all_clockins'])
    rec.reverse()
    print(rec)
    context['rec'] = rec

    return render(request, 'reports-employee.html', context)

# Process Single Employee Report
# Displays a single employees report
def process_employee_report(request, employee_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'employee': Employee.objects.get(id=employee_id),
        'all_clockins': ClockSystem.objects.filter(employee=employee_id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'res': [],
        'days_worked': "",
        'total_time_worked': ""
    }

    # getting data from context
    all_clockins = context['all_clockins']
    start_date = context['start_date']
    end_date = context['end_date']
    # setting all the filtered clockins to an array for use in report
    res = []
    # evaluating employee's clockins based on filtered dates
    for data in all_clockins:
        # setting string dates to datetime for evaluation
        s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        eval = datetime.datetime.strptime(str(data.date_in), "%Y-%m-%d")
        # evaluating our dates
        if s <= eval:
            if eval <= e:
                res.append(data)
    # Set data for report use
    context['res'] = res

    # Get Total Days Worked
    days_worked = str(len(res))
    context['days_worked'] = days_worked

    # Get Total Time worked
    now = datetime.datetime.now(pytz.timezone('US/Central'))
    datetimeFormat = '%H:%M:%S'
    # Getting time_worked for employee
    time_list = []
    for data in res:
        if not data.date_out:
            time_out = now.strftime("%H:%M:%S")
            date_out = now.strftime("%Y-%m-%d")
            dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
            dt_2 = str(date_out) + ' ' + str(time_out)
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            diff = datetime.datetime.strptime(dt_2, datetimeFormat) - datetime.datetime.strptime(dt_1, datetimeFormat)
            time_list.append(str(diff))
            data.date_out = now.strftime("%Y-%m-%d")
            data.clocked_out_at = str(time_out)
            data.time_worked = str(diff)
        else:
            time_list.append(data.time_worked)
    # Adding time worked for employee
    total_secs = 0
    for tm in time_list:
        time_parts = [int(s) for s in tm.split(':')]
        total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
    total_secs, sec = divmod(total_secs, 60)
    hr, min = divmod(total_secs, 60)
    total_time_worked = "%d:%02d:%02d" % (hr, min, sec)
    context['total_time_worked'] = total_time_worked

    res.reverse()
    context['res'] = res

    return render(request, 'report-employee-date-range.html', context)

# Process print employee report
# Prints an employees report
def process_employee_report_print(request, employee_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company.id),
        'employee': Employee.objects.get(id=employee_id),
        'all_clockins': ClockSystem.objects.filter(employee=employee_id),
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'res': [],
        'days_worked': "",
        'total_time_worked': ""
    }

    # getting data from context
    all_clockins = context['all_clockins']
    start_date = context['start_date']
    end_date = context['end_date']
    # setting all the filtered clockins to an array for use in report
    res = []
    # evaluating employee's clockins based on filtered dates
    for data in all_clockins:
        # setting string dates to datetime for evaluation
        s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        e = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        eval = datetime.datetime.strptime(str(data.date_in), "%Y-%m-%d")
        # evaluating our dates
        if s <= eval:
            if eval <= e:
                res.append(data)
    # Set data for report use
    context['res'] = res

    # Get Total Days Worked
    days_worked = str(len(res))
    context['days_worked'] = days_worked

    # Get Total Time worked
    now = datetime.datetime.now(pytz.timezone('US/Central'))
    datetimeFormat = '%H:%M:%S'
    # Getting time_worked for employee
    time_list = []
    for data in res:
        if not data.date_out:
            time_out = now.strftime("%H:%M:%S")
            date_out = now.strftime("%Y-%m-%d")
            dt_1 = str(data.date_in) + ' ' + str(data.clocked_in_at)
            dt_2 = str(date_out) + ' ' + str(time_out)
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            diff = datetime.datetime.strptime(dt_2, datetimeFormat) - datetime.datetime.strptime(dt_1, datetimeFormat)
            time_list.append(str(diff))
            data.date_out = now.strftime("%Y-%m-%d")
            data.clocked_out_at = str(time_out)
            data.time_worked = str(diff)
        else:
            time_list.append(data.time_worked)
    # Adding time worked for employee
    total_secs = 0
    for tm in time_list:
        time_parts = [int(s) for s in tm.split(':')]
        total_secs += (time_parts[0] * 60 + time_parts[1]) * 60 + time_parts[2]
    total_secs, sec = divmod(total_secs, 60)
    hr, min = divmod(total_secs, 60)
    total_time_worked = "%d:%02d:%02d" % (hr, min, sec)
    context['total_time_worked'] = total_time_worked

    res.reverse()
    context['rec'] = res
    print(context['rec'])


    return render(request, 'report-employee-print.html', context)


# =====================
# Edit/Delete Reports
# =====================

def edit_report(request, clockin_id):

    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])
    clock_in = ClockSystem.objects.get(id=clockin_id)

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company),
        'clock_in': clock_in,
    }

    return render(request, 'edit-report.html', context)

def process_edit_report(request, clockin_id):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')
    
    company = Company.objects.get(admins=request.session['admin_id'])

    context = {
        'company': company,
        'locations': Location.objects.filter(company=company),
        'clock_in': ClockSystem.objects.get(id=clockin_id)
    }
    employee = context['clock_in'].employee
    print(employee)
    # find employee
    all_employees = Employee.objects.filter(company=company)
    for e in all_employees:
        full_name = e.last_name + ', ' + e.first_name
        if full_name == employee:
            employee = e
    print(employee.id)
    clock_in = context['clock_in']
    print(clock_in.employee)
    clock_in.role = request.POST['role']
    clock_in.date_in = request.POST['date_in']
    clock_in.date_out = request.POST['date_out']
    clock_in.clocked_in_at = request.POST['clocked_in_at']
    clock_in.clocked_out_at = request.POST['clocked_out_at']
    clock_in.in_comment = request.POST['in_comment']
    clock_in.out_comment = request.POST['out_comment']
    # Get the location
    location = Location.objects.get(id=request.POST['location'])
    clock_in.location = location
    clock_in.flag_message = request.POST['flag_message']

    if request.POST['is_flagged'] == "True":
        clock_in.is_flagged = True
    if request.POST['is_flagged'] == "False":
        clock_in.is_flagged = False
    
    # Calculate hours_worked
    c_in = clock_in.clocked_in_at
    c_in += ':00'
    c_out = clock_in.clocked_out_at
    c_out += ':00'
    d_in = clock_in.date_in
    d_out = clock_in.date_out

    datetime1_str = str(d_in) + ' ' + c_in
    datetime2_str = str(d_out) + ' ' + c_out
    datetime1_str = str(d_in) + ' ' + c_in
    datetime2_str = str(d_out) + ' ' + c_out

    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    diff = datetime.datetime.strptime(datetime2_str, datetimeFormat) - datetime.datetime.strptime(datetime1_str, datetimeFormat)

    # Setting Time Worked
    clock_in.time_worked = str(diff)

    clock_in.save()

    return redirect(employee_report, employee_id=employee.id)

def process_delete_report(request):
    if 'admin_id' not in request.session:
        return redirect('/signin-company-admin')

    company = Company.objects.get(admins=request.session['admin_id'])
    
    clocksys_to_delete = ClockSystem.objects.get(id=request.POST['clockin_id'])
    all_employees = Employee.objects.filter(company=company)
    employee = clocksys_to_delete.employee
    print(employee)
    for e in all_employees:
        full_name = e.last_name + ', ' + e.first_name
        if full_name == employee:
            employee = e

    clocksys_to_delete.delete()

    return redirect(employee_report, employee_id=employee.id)

def process_delete_multiple_reports(request):
    pass 

