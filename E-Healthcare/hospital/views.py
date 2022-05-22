from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect
import time
import datetime
from django.utils import timezone
from django.core.mail import send_mail
# Create your views here.


def home(request):
    return render(request,'index.html')


def about(request):
    return render(request,'header.html')

def userLogin(request):
    error = ""
    if request.method=='POST':
        email_id=request.POST['email']
        print(email_id)
        pswd=request.POST['pass']
        user=authenticate(request,username=email_id,password=pswd)
        print(email_id)
        print(user)
        try:
            page = ""
            if user is not None:
                login(request, user)
                error = "no"
                g = request.user.groups.all()[0].name
                print('hello')
                print(g)
                if g == 'Doctor':
                    page = "doctor"
                    d = {'error': error, 'page': page}
                    return render(request, 'doctorhome.html', d)
                elif g == 'Patient':
                    page = "patient"
                    d = {'error': error, 'page': page}
                    return render(request, 'patienthome.html', d)
            else:
                error = "yes"
        except Exception as e:
            error = "yes"


    params={'error':error}
    return render(request,'login.html',params)

def createAccount(request):
    error=""
    user= "none"
    if request.method == 'POST':
        patient_name = request.POST['patient_name']
        email = request.POST['email']
        password = request.POST['pass']
        repeatpassword = request.POST['repeatPass']
        address = request.POST['address']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        bloodGroup = request.POST['bloodGroup']
        birthdate = request.POST['DOB']

        try:
            if password == repeatpassword:
                Patient.objects.create(patient_name=patient_name, email=email, address=address,
                                       mobile=mobile, gender=gender, DOB=birthdate, bloodGroup=bloodGroup)
                user = User.objects.create_user(first_name=patient_name, email=email, password=password, username=email)
                patientGroup = Group.objects.get(name='Patient')
                patientGroup.user_set.add(user)
                user.save()
                send_mail('test mail','thanks for using e-healthcare','jkaur2_be18@thapar.edu',
                           [email],fail_silently=False)
                error="no error"
            else:
                error="pass"

        except Exception as e:
            error = "account already existing"
            print(e)
    print(error)
    params={'error':error}
    return render(request,'createAccount.html',params)

def updateProfile(request):
    error = ""
    if not request.user.is_active:
        return redirect('login')
    g = request.user.groups.all()[0].name
    print(g)
    if g == 'Patient':
        if request.method == 'POST':
            patname = request.POST['patient_name']
            address = request.POST['address']
            mobile = request.POST['mobile']
            bloodGroup = request.POST['bloodGroup']
            birth = request.POST['Dob']
            birth1=birth.replace('.','')
            birth2 = birth1.replace(',', ' ')
            d2=datetime.datetime.strptime(birth2,'%b %d %Y').strftime('%Y-%m-%d')
            print(d2)
            try:

                patient_update = Patient.objects.get(email=request.user)
                patient_update.patient_name = patname
                patient_update.address=address
                patient_update.mobile =mobile
                patient_update.bloodGroup  = bloodGroup
                patient_update.DOB =d2
                patient_update.save()
                error = "no"
            except Exception as e:
                print("err is ", e)
                error = "yes"
                print(error)
            e = {"error": error}
            return render(request, 'patientupdate.html', e)

        elif request.method == 'GET':
            pat_old = Patient.objects.all().filter(email=request.user)
            d = {'patient_details': pat_old}
            return render(request, 'patientupdate.html', d)

    elif g == 'Doctor':
        if request.method == 'POST':
            docname = request.POST['doctor_name']
            address = request.POST['address']
            mobile = request.POST['mobile']
            bloodGroup = request.POST['bloodGroup']
            birth = request.POST['Dob']
            birth1 = birth.replace('.', '')
            birth2 = birth1.replace(',', ' ')
            d2 = datetime.datetime.strptime(birth2, '%b %d %Y').strftime('%Y-%m-%d')
            print(d2)
            try:

                doc_update = Doctor.objects.get(email=request.user)
                doc_update.doctor_name = docname
                doc_update.address = address
                doc_update.mobile = mobile
                doc_update.bloodGroup = bloodGroup
                doc_update.DOB = d2
                doc_update.save()
                error = "no"
            except Exception as e:
                print("err is ", e)
                error = "yes"
                print(error)
            e = {"error": error}
            return render(request, 'doctorupdate.html', e)

        elif request.method == 'GET':
            doc_old = Doctor.objects.all().filter(email=request.user)
            d = {'doctor_details': doc_old}
            return render(request, 'doctorupdate.html', d)


def userLogout(request):
    logout(request)
    return redirect('login')



def contactUs(request):
    return render(request,'contact.html')


def dashboard(request):
    if not request.user.is_active:
        return redirect('login')

    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        return render(request, 'doctorhome.html')

    elif g == 'Patient':
        return render(request, 'patienthome.html')



def profile(request):
    if not request.user.is_active:
        return redirect('login')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(email=request.user)

        d = {'patient_details': patient_details}
        print(d)
        return render(request, 'profile_patient.html', d)

    elif g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(email=request.user)
        d = {'doctor_details': doctor_details}
        return render(request, 'profile_doctor.html', d)


def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('login')
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        if request.method == 'POST':

            doctoremail = request.POST['doctoremail']
            doctorname = request.POST['doctorname']
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            try:
                Appointment.objects.create(patient_name=patientname, doctor_name=doctorname, p_email=patientemail,
                                          d_email=doctoremail,appoint_date=appointmentdate, appoint_time=appointmenttime, symptoms=symptoms,
                                          prescription="",status=True)
                body_mail='You have an appointment scheduled on '+appointmentdate+'\nTime:'+appointmenttime+'\nDoctor:'+doctorname
                send_mail('test mail-appointment',body_mail, 'jkaur2_be18@thapar.edu',
                          [patientemail], fail_silently=False)
                error = "no"
            except Exception as e:
                print("err is ",e)
                error = "yes"
            e = {"error": error}
            return render(request, 'patientmakeappointment.html', e)
        elif request.method == 'GET':
            return render(request, 'patientmakeappointment.html', d)



def ViewAppointments(request):
    if not request.user.is_active:
        return redirect('login')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        upcoming_appointments = Appointment.objects.filter(p_email=request.user,
                                                           appoint_date__gte=timezone.now(), status=True).order_by('appoint_date')
        previous_appointments = Appointment.objects.filter(p_email=request.user,
                                                           appoint_date__lt=timezone.now()).order_by('-appoint_date') | Appointment.objects.filter(p_email=request.user, status=False).order_by(
            '-appoint_date')
        d = {"upcoming_appointments": upcoming_appointments, "previous_appointments": previous_appointments}
        return render(request, 'patient_view_appoints.html', d)

    elif g == 'Doctor':
        if request.method == 'POST':
            prescriptiondata = request.POST['prescription']
            idvalue = request.POST['idofappointment']
            Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata, status=False)

        upcoming_appointments = Appointment.objects.filter(d_email=request.user,
                                                           appoint_date__gte=timezone.now(), status=True).order_by('appoint_date')
        previous_appointments = Appointment.objects.filter(d_email=request.user,
                                                           appoint_date__lt=timezone.now()).order_by('-appoint_date') | Appointment.objects.filter(d_email=request.user, status=False).order_by(
            '-appoint_date')
        d = {"upcoming_appointments": upcoming_appointments, "previous_appointments": previous_appointments}
        return render(request, 'doctor_view_appoints.html', d)


def patient_delete_appointment(request, pid):
    if not request.user.is_active:
        return redirect('loginpage')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('viewappoint')


def Login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminlogin.html', d)

def adminaddDoctor(request):
    error = ""
    user = "none"
    if not request.user.is_staff:
        return redirect('login_admin')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpasssword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        specialization = request.POST['specialization']

        try:
            if password == repeatpassword:
                Doctor.objects.create(doctor_name=name, email=email,address=address, mobile=phonenumber,gender=gender,
                                       bloodGroup=bloodgroup,DOB=birthdate,  specialization=specialization)

                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                doc_group = Group.objects.get(name='Doctor')
                doc_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminadddoctor.html', d)


def adminviewDoctor(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'adminviewdocs.html', d)


def admin_delete_doctor(request, pid, email):
    if not request.user.is_staff:
        return redirect('login_admin')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    users = User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewDoctor')

def adminviewAppointment(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    upcoming_appointments = Appointment.objects.filter(appoint_date__gte=timezone.now(), status=True).order_by(
        'appoint_date')
    # print("Upcomming Appointment",upcomming_appointments)
    previous_appointments = Appointment.objects.filter(appoint_date__lt=timezone.now()).order_by(
        '-appoint_date') | Appointment.objects.filter(status=False).order_by('-appoint_date')
    # print("Previous Appointment",previous_appointments)
    d = {"upcoming_appointments": upcoming_appointments, "previous_appointments": previous_appointments}
    return render(request, 'adminviewappointments.html', d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    logout(request)
    return redirect('login_admin')


def AdminHome(request):
    # after login user comes to this page.
    if not request.user.is_staff:
        return redirect('login_admin')
    return render(request, 'adminhome.html')
