from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('features/',views.feature,name='features'),
    path('result/',views.result,name='result'),
    path('result/marks/',views.marks,name='marks'),
    path('teacher_login/',views.tech_login,name='tech_login'),
    path('teacher_signup/',views.tech_signup,name='tech_signup'),
    path('students_login/',views.std_login,name='std_login')
]