from django.shortcuts import render,redirect
from django.http import HttpResponse
from student.models import Student,Marks
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import teacher

# Create your views here.
@login_required
def tech_index(request):
    context={}
    user = request.user.username
    data = teacher.objects.get(username=user)
    context['data']=data
    return render(request,'Tech_index.html',context)

@login_required
def tech_home(request):
    context = {}
    user = request.user.username
    data = teacher.objects.get(username=user)
    context['data']=data
    std = Student.objects.all().order_by('Std_Id')
    context['std']=std
    
    return render(request,'Tech_dashboard.html',context)

@login_required
def tech_create(request):
    context = {}
    user = request.user.username
    data = teacher.objects.get(username=user)
    context['data']=data
    if request.method == 'GET':
        return render(request, 'tech_fill.html',context)
    elif request.method == 'POST':
        std_id = request.POST.get('std_id')
        std_name = request.POST.get('std_name')
        std_father = request.POST.get('std_father')
        std_mother = request.POST.get('std_mother')
        std_nationality = request.POST.get('std_nationality')
        std_category = request.POST.get('std_category')
        std_rollno = request.POST.get('std_rollno')
        std_address1 = request.POST.get('std_address1')
        std_checkbox = request.POST.get('std_checkbox')
        if std_checkbox is None:
            std_checkbox = False
        else:
            std_checkbox = True
        
        if std_id =='' or std_name =='' or std_father=='' or std_mother=='' or std_nationality=='' or std_address1 =='' or std_category=='' or std_rollno=='':
            context['message'] = 'Please fill all the details'
        else:
            try:
                uid = request.user.username
                teach = teacher.objects.get(username=uid)
                existing_student = Student.objects.filter(Roll_No=std_rollno, Std=teach.std).exists()
                if existing_student:
                    context['message'] = 'Student with roll number already exists in this class'
                else:
                    data = Student(
                        tech_name=teach,
                        Std_Id=std_id,
                        Full_Name=std_name,
                        Father=std_father,
                        Mother=std_mother,
                        Nationality=std_nationality,
                        Category=std_category,
                        Roll_No=std_rollno,
                        Residental_Add=std_address1,
                        Std = teach.std,
                        Div = teach.div,
                        Board_Code = teach.board,
                        Fee_Status = std_checkbox 
                    )
                    data.save()
                    
                    context['message'] = 'Student added successfully'
            except IntegrityError:
                context['message'] = 'Error: Student with the same Id already exists'
            
    return render(request, 'tech_fill.html', context)

@login_required
def tech_marks(request):
    context = {}
    user = request.user.username
    data = teacher.objects.get(username=user)
    context['data']=data
    if request.method == 'GET':
        return render(request, 'tech_marks.html',context)
    elif request.method == 'POST':
        std_id = request.POST.get('std_idno')
        tar = request.POST.get('tar')
        scr = request.POST.get('scr')
        english = request.POST.get('english')
        hindi = request.POST.get('hindi')
        marathi = request.POST.get('marathi')
        science = request.POST.get('science')
        maths = request.POST.get('maths')
        social = request.POST.get('social')

        try:
            tar1 = int(tar)
            english1 = int(english)
            hindi1 = int(hindi)
            marathi1 = int(marathi)
            science1 = int(science)
            maths1 = int(maths)
            social1 = int(social)
        except ValueError:
            context['message'] = 'Please enter the student id.'

        # Check if the student exists
        student_exists = Student.objects.filter(Std_Id=std_id).exists()
        if student_exists:
            if std_id == '' or tar == '' or scr == '' or english == '' or hindi == '' or marathi == '' or science == '' or maths == '' or social == '' or tar =='' or scr =='':
                context['message'] = 'Please fill all the details'
            elif(english1 > tar1 or hindi1 > tar1 or marathi1 > tar1 or science1 > tar1 or maths1 > tar1 or social1 > tar1):
                context['message'] = 'Entered marks is greater than total marks'
                print('greater1')
            else:
                student = Student.objects.get(Std_Id=std_id)
                marks_object,created = Marks.objects.update_or_create(
                Sid=student,
                defaults={
                    'English': english,
                    'Hindi': hindi,
                    'Marathi': marathi,
                    'Science': science,
                    'Mathematics': maths,
                    'SocialScience': social,
                    'target': tar,
                    'score': scr
                    }
                    )
                if created:
                    context['message'] = 'Marks created successfully'
                else:
                    context['message'] = 'Marks updated successfully'
        else:
            context['message'] = 'Student with the provided ID does not exist'                

    return render(request, 'tech_marks.html', context)

@login_required
def tech_std(request):
    context = {}
    uid = request.user.username
    data = teacher.objects.get(username=uid)
    context['data']=data
    u = Student.objects.filter(tech_name=data).order_by('Roll_No')
    student_marks = []
    for student in u:
        has_marks = Marks.objects.filter(Sid=student).exists()
        student_marks.append({
            'student': student,
            'has_marks': has_marks
        })
    context['std']=student_marks
    return render(request,'tech_std.html',context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def delete_student(request, student_id):
    # Get the student object
    student = Student.objects.get(id=student_id)
    # Delete marks associated with the student (if any)
    Marks.objects.filter(Sid=student).delete()
    student.delete()
    return redirect('tech_std') 

@login_required
def tech_edit(request,std_id):
    context = {}
    student = Student.objects.get(id=std_id)
    context['student'] = student
    uid = request.user.username
    data = teacher.objects.get(username=uid)
    context['data']=data
    if request.method == 'GET':
        return render(request, 'tech_edit.html',context)
    elif request.method == 'POST':
        std_no1 = request.POST.get('std_no1')
        std_no2 = request.POST.get('std_no2') 
        std_checkbox = request.POST.get('std_checkbox')
        if std_checkbox is None:
            std_checkbox = False
        else:
            std_checkbox = True


        if (std_no1 and len(std_no1) != 10) or (std_no2 and len(std_no2) != 10):
            context['error'] = "Mobile numbers must be exactly 10 digits."
        else:

            student.Fee_Status = std_checkbox
            student.Full_Name = request.POST.get('std_name') or student.Full_Name
            student.Roll_No = request.POST.get('std_rollno') or student.Roll_No
            student.Nationality = request.POST.get('std_nationality') or student.Nationality
            student.Std = request.POST.get('std_std') or student.Std
            student.Div = request.POST.get('std_div') or student.Div
            student.Email = request.POST.get('std_email') or student.Email
            student.Category = request.POST.get('std_category') or student.Category
            student.Father = request.POST.get('std_father') or student.Father
            student.Mother = request.POST.get('std_mother') or student.Mother
            student.Father_No = std_no1 or student.Father_No
            student.Mother_No = std_no2 or student.Mother_No 
            student.Father_Job = request.POST.get('std_job1') or student.Father_Job
            student.Mother_Job = request.POST.get('std_job2') or student.Mother_Job 
            student.Board_Code = request.POST.get('std_board') or student.Board_Code
            student.Residental_Add = request.POST.get('res_address') or student.Residental_Add
            student.Parmanenet_Add = request.POST.get('par_address') or student.Parmanenet_Add
        
            student.save()
            return redirect('tech_std')

    return render(request,'tech_edit.html',context)
