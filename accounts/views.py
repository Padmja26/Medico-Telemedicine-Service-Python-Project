# Import necessary Django modules and models
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User, auth
from main_app.models import patient, doctor
from datetime import datetime

# Create your views here.

# View function for logging out a user
def logout(request):
    auth.logout(request)
    request.session.pop('patientid', None)
    request.session.pop('doctorid', None)
    request.session.pop('adminid', None)
    return render(request, 'homepage/index.html')

# View function for admin sign-in
def sign_in_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                if user.is_superuser == True:
                    auth.login(request, user)
                    return redirect('admin_ui')
            except:
                messages.info(request, 'Please enter the correct username and password for an admin account.')
                return redirect('sign_in_admin')
        else:
            messages.info(request, 'Please enter the correct username and password for an admin account.')
            return redirect('sign_in_admin')
    else:
        return render(request, 'admin/signin/signin.html')

# View function for patient sign-up
def signup_patient(request):
    if request.method == 'POST':
        if all(request.POST.get(field) for field in ['username', 'email', 'name', 'dob', 'gender', 'address', 'mobile', 'password', 'password1']):
            username = request.POST['username']
            email = request.POST['email']
            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            address = request.POST['address']
            mobile_no = request.POST['mobile']
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('signup_patient')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken')
                    return redirect('signup_patient')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    patientnew = patient(user=user, name=name, dob=dob, gender=gender, address=address, mobile_no=mobile_no)
                    patientnew.save()
                    messages.info(request, 'User created successfully')
                return redirect('sign_in_patient')
            else:
                messages.info(request, 'Passwords do not match, please try again')
                return redirect('signup_patient')
        else:
            messages.info(request, 'Please make sure all required fields are filled out correctly')
            return redirect('signup_patient')
    else:
        return render(request, 'patient/signup_Form/signup.html')

# View function for patient sign-in
def sign_in_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                if user.patient.is_patient == True:
                    auth.login(request, user)
                    request.session['patientusername'] = user.username
                    return redirect('patient_ui')
            except:
                messages.info(request, 'Invalid credentials')
                return redirect('sign_in_patient')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('sign_in_patient')
    else:
        return render(request, 'patient/signin_page/index.html')

# View function for saving patient data
def savepdata(request, patientusername):
    if request.method == 'POST':
        name = request.POST['name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        mobile_no = request.POST['mobile_no']
        dobdate = datetime.strptime(dob, '%Y-%m-%d')
        puser = User.objects.get(username=patientusername)
        patient.objects.filter(pk=puser.patient).update(name=name, dob=dobdate, gender=gender, address=address, mobile_no=mobile_no)
        return redirect('pviewprofile', patientusername)

# View function for doctor sign-up
def signup_doctor(request):
    if request.method == 'GET':
        return render(request, 'doctor/signup_Form/signup.html')
    if request.method == 'POST':
        if all(request.POST.get(field) for field in ['username', 'email', 'name', 'dob', 'gender', 'address', 'mobile', 'password', 'password1', 'registration_no', 'year_of_registration', 'qualification', 'State_Medical_Council', 'specialization']):
            username = request.POST['username']
            email = request.POST['email']
            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            address = request.POST['address']
            mobile_no = request.POST['mobile']
            registration_no = request.POST['registration_no']
            year_of_registration = request.POST['year_of_registration']
            qualification = request.POST['qualification']
            State_Medical_Council = request.POST['State_Medical_Council']
            specialization = request.POST['specialization']
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('signup_doctor')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken')
                    return redirect('signup_doctor')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    doctornew = doctor(user=user, name=name, dob=dob, gender=gender, address=address, mobile_no=mobile_no, registration_no=registration_no, year_of_registration=year_of_registration, qualification=qualification, State_Medical_Council=State_Medical_Council, specialization=specialization)
                    doctornew.save()
                    messages.info(request, 'User created successfully')
                return redirect('sign_in_doctor')
            else:
                messages.info(request, 'Passwords do not match, please try again')
                return redirect('signup_doctor')
        else:
            messages.info(request, 'Please make sure all required fields are filled out correctly')
            return redirect('signup_doctor')

# View function for doctor sign-in
def sign_in_doctor(request):
    if request.method == 'GET':
        return render(request, 'doctor/signin_page/index.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                if user.doctor.is_doctor == True:
                    auth.login(request, user)
                    request.session['doctorusername'] = user.username
                    return redirect('doctor_ui')
            except:
                messages.info(request, 'Invalid credentials')
                return redirect('sign_in_doctor')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('sign_in_doctor')
    else:
        return render(request, 'doctor/signin_page/index.html')

# View function for saving doctor data
def saveddata(request, doctorusername):
    if request.method == 'POST':
        name = request.POST['name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        mobile_no = request.POST['mobile_no']
        registration_no = request.POST['registration_no']
        year_of_registration = request.POST['year_of_registration']
        qualification = request.POST['qualification']
        State_Medical_Council = request.POST['State_Medical_Council']
        specialization = request.POST['specialization']
        dobdate = datetime.strptime(dob, '%Y-%m-%d')
        yor = datetime.strptime(year_of_registration, '%Y-%m-%d')
        duser = User.objects.get(username=doctorusername)
        doctor.objects.filter(pk=duser.doctor).update(name=name, dob=dob, gender=gender, address=address, mobile_no=mobile_no, registration_no=registration_no, year_of_registration=yor, qualification=qualification, State_Medical_Council=State_Medical_Council, specialization=specialization)
        return redirect('dviewprofile', doctorusername)
