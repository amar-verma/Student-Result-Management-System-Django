from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.tech_home,name='tech_home'),
    path('teacher_create/',views.tech_create,name='tech_create'),
    path('teacher_marks/',views.tech_marks,name='tech_marks'),
    path('teacher_students/',views.tech_std,name='tech_std'),
    path('index/',views.tech_index, name='index'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('delete_student/<int:student_id>/',views.delete_student,name='delete_student'),
    path('tech_edit/<int:std_id>/',views.tech_edit,name='tech_edit')
]