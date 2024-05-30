from django.db import models
from Teacher.models import teacher
# Create your models here.
class Student(models.Model):
    tech_name = models.ForeignKey(teacher, on_delete=models.CASCADE,db_column='tech_name',null=True)
    Std_Id = models.CharField(max_length=10,default=0,unique=True)
    Roll_No = models.IntegerField(null=True)
    Full_Name = models.CharField(max_length=75)
    Nationality = models.CharField(max_length=25)
    Std = models.IntegerField(null=True)
    Div = models.CharField(max_length=3)
    Email = models.EmailField()
    Category = models.CharField(max_length=25)
    Father = models.CharField(max_length=50)
    Mother = models.CharField(max_length=50)
    Father_No = models.IntegerField(null=True)
    Mother_No = models.IntegerField(null=True)
    Father_Job = models.CharField(max_length=50)
    Mother_Job = models.CharField(max_length=50)
    Board_Code  = models.CharField(max_length=25)
    Residental_Add = models.TextField(null=True)
    Parmanenet_Add = models.TextField(null=True)
    Fee_Status = models.BooleanField(default=False)
    

    def __str__(self):
        return self.Std_Id

class Marks(models.Model):
    Sid = models.ForeignKey(Student,on_delete=models.CASCADE,db_column='Sid')
    English = models.IntegerField()
    Hindi = models.IntegerField()
    Marathi = models.IntegerField()
    Science = models.IntegerField()
    Mathematics = models.IntegerField()
    SocialScience = models.IntegerField()
    target = models.IntegerField(default=100)
    score = models.IntegerField()


    def __str__(self):
        return str(self.Sid)
    
