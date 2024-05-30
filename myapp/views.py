from django.shortcuts import render,redirect
from django.http import HttpResponse
from student.models import Student,Marks
from Teacher.models import teacher
from student import views,urls
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from Teacher import urls
from student import urls
# Create your views here.

def home(request):
    return render(request,'home.html')

def feature(request):
    return render(request,'features.html')


def result(request):
    context = {}
    if request.method == 'GET':
        # Clear the student ID from session
        if 'std_id' in request.session:
            del request.session['std_id']
        return render(request, 'result.html')
    else:
        std_id = request.POST.get('std_id')
        std_mother = request.POST.get('std_mother')

        if std_id == '' or std_mother == '':
            context['message'] = 'Please enter all the details'
        else:
            try:
                s = Student.objects.get(Std_Id=std_id, Mother=std_mother)
                m = Marks.objects.get(Sid=s)
                # Store std_id in session
                request.session['std_id'] = std_id
                return redirect('marks')
            except Student.DoesNotExist:
                context['message'] = 'Unable to fetch data'
            except Marks.DoesNotExist:
                context['message'] = 'No marks found for the provided student ID'
        
        return render(request, 'result.html', context)


def marks(request):
    context={}
    std_id = request.session.get('std_id')
    if not std_id:
        # If std_id is not found in session, redirect to result page
        return redirect('result')
    try:
        student = Student.objects.get(Std_Id=std_id)
        mark = Marks.objects.get(Sid=student)
        context['student'] = student
        context['m'] = mark
        sum = int(mark.English) + int(mark.Hindi) +int(mark.Science)  + int(mark.Marathi) + int(mark.SocialScience) + int(mark.Mathematics)
        context['sum'] = sum
        total = int(mark.target)*6
        context['total']=total
        if int(mark.English) < int(mark.score) or int(mark.Hindi) < int(mark.score) or int(mark.Science) < int(mark.score) or int(mark.Marathi) < int(mark.score) or int(mark.SocialScience) < int(mark.score) or int(mark.Mathematics) < int(mark.score) :
            context['status'] ='Fail'
        else:
            context['status']= 'Pass'
    except Student.DoesNotExist:
        # If the student does not exist, redirect to result page with a message
        context['message']='Student data not found'
    except Marks.DoesNotExist:
        context['message'] = 'No marks found for the provided student ID'
        return redirect('result')

    return render(request, 'marks.html', context)




def std_login(request):
    context = {}
    if request.method == 'GET':
        # Clear the student ID from session
        if 'student_data' in request.session:
            del request.session['student_data']
        return render(request, 'Std_login.html')
    else:
        uname = request.POST.get('std_id')
        upass = request.POST.get('password')

        if not uname or not upass:
            context['error'] = "Please fill all the fields"
        else:
            try:
                student = Student.objects.get(Std_Id=uname)
                if student and student.Std_Id == upass: 
                    request.session['student_data'] = student.id
                    return redirect('std_dashboard')
                else:
                    context['error'] = 'Invalid student ID or password'
            except Student.DoesNotExist:
                context['error'] = 'Invalid student ID or password'

        return render(request, 'Std_login.html', context)
    



def tech_login(request):
    context ={}
    if(request.method=='GET'):
        return render(request,'Tech_Login.html')
    else:
        uname = request.POST['uname']
        upass = request.POST['upass']
        if uname=="" or upass=="":
            context['message']="please fill all the fields"
        else:
            u = authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('tech_home')
            else:
                context['message']='Invalid User'
        return render(request,'Tech_Login.html',context)
    

def tech_signup(request):
    context = {}
    if request.method=='GET':
        return render(request,'Tech_SignUp.html')
    else:
        uname = request.POST.get('uname')
        upass = request.POST.get('upass')
        upass1 = request.POST.get('upass1')
        tech_name = request.POST.get('tech_name')
        tech_div = request.POST.get('tech_div')
        tech_class = request.POST.get('tech_class')
        tech_board = request.POST.get('tech_board')

        if uname =='' or upass =='' or upass1 =='' or tech_name =='' or tech_div =='' or tech_class =='' or tech_board =='':
            context['message']='please enter all the details'
        elif upass != upass1:
            context['message']='password does not match'
        else:
            try:
                #error occur if data is not in database that's why we create expections handling..
                name = User.objects.get(username=uname) 
                context['message']='username already exisits'
            except User.DoesNotExist:
                my_user = User.objects.create(password=upass, username=uname)
                my_user.set_password(upass)
                my_user.save()
                data = teacher(
                    username = uname,
                    name = tech_name,
                    div = tech_div,
                    std = tech_class,
                    board = tech_board
                )
                data.save()
                return redirect('home')
            
        return render(request,'Tech_SignUp.html',context)
    