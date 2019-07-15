from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views
from .models import PresentSheet
from rest_framework.routers import DefaultRouter
from django.urls import reverse_lazy
from django.conf import settings

# attendance_api_link object  !!! Will be bugged!!!
obj = PresentSheet.objects.all()
if obj.exists():
    a = PresentSheet.objects.last()
    session =a.select_session
    course_code =a.select_course_code
    random_url =a.random_url

# API codes
router = DefaultRouter()     
router.register('hello-viewset', views.HelloViewSet, base_name='hello_viewset')
router.register('profile', views.UserProfileViewSet)
router.register('student-profile', views.StudentProfileViewSet)
router.register('course-presentsheet',views.CoursePresentSheetViewSet, base_name='course-presentsheet')
# router.register('course-percentage',views.CoursePercentageViewSet, base_name='course-percentage')

app_name = "accounts"
    
urlpatterns = [
    path('',views.first, name='first'),
    path('qrcodeattendance/', views.qrcodeattendance, name='qrcodeattendance'),
    path('qrcodeattendance/login/', views.login_views, name='login'),
    path('qrcodeattendance/logout/', views.logout_views, name='logout'),
    path('qrcodeattendance/signup/', views.register, name='signup'), # for teacher
    path('qrcodeattendance/student_signup/', views.student_signup, name='student_signup'),
    path('qrcodeattendance/admin_profile/',views.view_admin_profile, name='view_admin_profile'),
    path('qrcodeattendance/profile/', views.view_profile, name='profile'), # for teacher
    path('qrcodeattendance/student_profile/', views.view_student_profile, name='student_profile'), # for teacher
    re_path('qrcodeattendance/teacher/(?P<student>[a-zA-Z0-9-_]+)/$', views.view_teacher_student_profile, name='view_teacher_student_profile'),
    path('qrcodeattendance/edit_profile/',views.edit_profile, name='edit_profile'), # for edit profile  
    
    #Delete urls
    re_path('qrcodeattendance/profile/(?P<course_code>[a-zA-Z0-9-_]+)/delete/', views.delete_course_attendance_details, name='delete_course_attendance_details'),
    re_path('qrcodeattendance/profile/(?P<course_code>[a-zA-Z0-9-_]+)/(?P<random_url>[a-zA-Z0-9_]+)/sheet-delete', views.delete_course_attendance_sheet, name='delete_course_attendance_sheet'),

    re_path('^qrcodeattendance/profile/(?P<random_url>[a-zA-Z0-9-_]+)/$', views.present_sheet, name='present_sheet'), 
    re_path('^qrcodeattendance/profile/(?P<course_code>[a-zA-Z0-9-_]+)/(?P<session>[a-zA-Z0-9-_]+)/(?P<student>[a-zA-Z0-9-_]+)/$',views.course_percentage, name='course_percentage'),
    re_path('^qrcodeattendance/profile/session/(?P<slug>[-\w]+)/$', views.view_session, name='session'),
    re_path('^qrcodeattendance/profile/session/(?P<slug>[a-zA-Z0-9-_]+)/(?P<course_code>[a-zA-Z0-9-_]+)/qr_code/(?P<random_url>[a-zA-Z0-9-_]+)/$', views.view_qr_code, name='view_qr_code'),
    re_path('^qrcodeattendance/profile/(?P<course_code>[a-zA-Z0-9-_]+)/presentsheet/',views.course_present_sheet, name='course_present_sheet'),
 
    #API urlsx
    re_path('qrcodeattendance/profile/session/(?P<session>[a-zA-Z0-9-_]+)/(?P<course_code>[a-zA-Z0-9-_]+)/qr_code_api/(?P<random_url>[a-zA-Z0-9-_]+)', views.AttendanceSheetView.as_view()),
    path('api-course-percentage/', views.CoursePercentage.as_view()),
    path('api-login/', views.LoginViewSet.as_view()),
    path('api-logout/', views.LogoutView.as_view()),
    path('api/',include(router.urls)),
]   