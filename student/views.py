from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Student,Marks
from . import template
from django.db.models import Sum
import json
from django.core.exceptions import ObjectDoesNotExist
from weasyprint import HTML
from django.template.loader import render_to_string
import random
import razorpay
from razorpay.errors import BadRequestError
from django.core.mail import send_mail

# Create your views here.
def std_index(request):
    context={}
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        context['student']=student
    return render(request,'std_index.html')


def std_dashboard(request):
    context={}
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        marks_exist = Marks.objects.filter(Sid=student).exists()
        if (student.Full_Name and student.Roll_No and student.Std and student.Div and  student.Nationality and student.Father and student.Mother and student.Board_Code and student.Residental_Add and student.Email and student.Category and student.Father_No and student.Mother_No and student.Father_Job and student.Mother_Job and student.Parmanenet_Add):
            context['message']='Complete'
        else:
            context['message']='InComplete'
        context['student']=student
        context['marks_exist']=marks_exist
    return render(request, 'std_dashboard.html', context)

def std_details(request):
    context={}
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        context['student']=student

    return render(request,'std_details.html',context)

def std_dedit(request):
    context={}
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        context['student']=student
        if request.method == 'GET':
            return render(request, 'std_dedit.html',context)
        elif request.method == 'POST':
            std_name = request.POST.get('std_name')
            std_rollno = request.POST.get('std_rollno')
            std_nationality = request.POST.get('std_nationality')
            std_std = request.POST.get('std_std')
            std_div = request.POST.get('std_div')
            std_category = request.POST.get('std_category')
            std_father = request.POST.get('std_father')
            std_mother = request.POST.get('std_mother')
            std_no1 = request.POST.get('std_no1')
            std_no2 = request.POST.get('std_no2')
            std_board = request.POST.get('std_board')
            res_address = request.POST.get('res_address')


            if not std_name or not std_rollno or not std_nationality or not std_std or not std_div or not std_category or not std_father or not std_mother or not std_no1 or not std_board or not res_address:
                context['error'] = "Please fill all the necessary fields."
                return render(request, 'std_dedit.html', context)
            elif (std_no1 and len(std_no1) != 10) or (std_no2 and len(std_no2) != 10):
                context['error'] = "Mobile numbers must be exactly 10 digits."
                return render(request, 'std_dedit.html', context)
            else:
                student.Full_Name = std_name or student.Full_Name
                student.Roll_No = student.Roll_No
                student.Nationality = student.Nationality
                student.Std = student.Std
                student.Div = student.Div
                student.Email = request.POST.get('std_email') or student.Email
                student.Category = student.Category
                student.Father = std_father or student.Father
                student.Mother = std_mother or student.Mother
                student.Father_No = std_no1 or student.Father_No
                student.Mother_No = std_no2 or student.Mother_No
                student.Father_Job = request.POST.get('std_job1') or student.Father_Job
                student.Mother_Job = request.POST.get('std_job2') or student.Mother_Job
                student.Board_Code = student.Board_Code
                student.Residental_Add = res_address or student.Residental_Add
                student.Parmanenet_Add = request.POST.get('par_address') or student.Parmanenet_Add

                student.save()
                return redirect('std_details')

    return render(request, 'std_dedit.html', context)


def std_marks(request):
    context={}
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        marks_exist = Marks.objects.filter(Sid=student)
        
        if marks_exist:
            mark = Marks.objects.get(Sid=student)
            marks_data = {
                'Mathematics': mark.Mathematics,
                'Science': mark.Science,
                'English': mark.English,
                'Hindi': mark.Hindi,
                'Marathi': mark.Marathi,
                'SocialScience': mark.SocialScience
            }
            context['marks_data'] = json.dumps(marks_data)
            context['mark']=mark
        else:
            context['data']='Your Marks has not been Uploaded yet..'
            
        context['student']=student
        context['marks_exist']=marks_exist
    return render(request,'std_marks.html',context)


def std_logout(request):
    if 'student_data' in request.session:
        del request.session['student_data']
    return redirect('home')


def marksheet(request):
    context = {}
    student_data = request.session.get('student_data')
    try:

        student = Student.objects.get(id=student_data)
        mark = Marks.objects.get(Sid=student)
        sum = (int(mark.English) + int(mark.Hindi) + int(mark.Science) + int(mark.Marathi) + int(mark.SocialScience) + int(mark.Mathematics))
        total = int(mark.target) * 6
        per = (sum / total) * 100
        per = round(per, 2)
        context['student'] = student
        context['mark'] = mark
        context['sum'] = sum
        context['total'] = total
        context['per'] = per

        if (int(mark.English) < int(mark.score) or int(mark.Hindi) < int(mark.score) or int(mark.Science) < int(mark.score) or int(mark.Marathi) < int(mark.score) or int(mark.SocialScience) < int(mark.score) or int(mark.Mathematics) < int(mark.score)):
            context['status'] = 'Fail'
        else:
            context['status'] = 'Pass'
        html_string = render_to_string('marksheet.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="marksheet.pdf"'
        response.write(pdf)
        return response
    except Student.DoesNotExist:
        return redirect('/')
    except Marks.DoesNotExist:
        return redirect('std_dashboard')


def std_payment(request):
    context={}
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        context['student'] = student
        pay_id = str(random.randrange(1000,9999))
        sum = 100
        context['sum'] = sum
        client = razorpay.Client(auth=("rzp_test_XXXXXxxxxxXXX", "xxxxXxxxXxXXxXxxXXx"))
        try:
            data = { "amount": sum * 100, "currency": "INR", "receipt": pay_id }  # amount should be in paise
            payment = client.order.create(data=data)
            context['payment'] = payment
        except BadRequestError as e:
            context['error'] = "There was an error processing your payment. Please try again."


    return render(request,'std_payment.html',context)

def std_fee(request):
    student_data = request.session.get('student_data')
    if not student_data:
        return redirect('std_login')
    else:
        student = Student.objects.get(id=student_data)
        student.Fee_Status = True
        student.save()
    return redirect('std_marks')