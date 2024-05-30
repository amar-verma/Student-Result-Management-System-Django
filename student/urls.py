from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('student_dashboard/',views.std_dashboard,name='std_dashboard'),
    path('student_detail/',views.std_details,name='std_details'),
    path('student_dedit/',views.std_dedit,name='std_dedit'),
    path('student_marks/',views.std_marks,name='std_marks'),
    path('studentd_logout/',views.std_logout,name='std_logout'),
    path('student_payment/',views.std_payment,name='std_payment'),
    path('marksheet/',views.marksheet,name='marksheet'),
    path('std_fee/',views.std_fee, name='std_fee')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)