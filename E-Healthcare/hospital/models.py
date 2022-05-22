from django.db import models

# Create your models here.


class Patient(models.Model):
    patient_no=models.AutoField
    patient_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    address=models.CharField(max_length=120)
    mobile=models.CharField(max_length=10)
    gender=models.CharField(max_length=15)
    bloodGroup=models.CharField(max_length=4)
    DOB=models.DateField()

    def __str__(self):
        return self.patient_name


class Doctor(models.Model):
    doctor_no = models.AutoField
    doctor_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=120)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=15)
    bloodGroup = models.CharField(max_length=4)
    DOB = models.DateField()
    specialization=models.CharField(max_length=40)

    def __str__(self):
        return self.doctor_name


class Appointment(models.Model):
    patient_name = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=50)
    p_email = models.EmailField()
    d_email=models.EmailField()
    appoint_date=models.DateField()
    appoint_time=models.TimeField()
    symptoms=models.CharField(max_length=120)
    prescription =models.CharField(max_length=300)
    status=models.BooleanField()

    def __str__(self):
        return self.patient_name+" :You have Appointment with "+self.doctor_name

