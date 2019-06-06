from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from accounts.forms import RegistrationForm, EditProfileForm, AdditionalInfoForm, StudentSignUpForm 
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.models  import User
from .models import ClassSession, CourseCode, UserProfile, StudentProfile, PresentSheet, TeacherProfile, CoursePercentage
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib import messages

# Import API classes, methods (THIRD PARTY)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication 
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer #for login APIView
from rest_framework.authtoken.views import ObtainAuthToken #for login APIView


# Import API classes, methods (LOCAL)
from . import serializers
from . import permissions

# Create your views here.

# def main(request): # Need to work! (Waiting)
#     if request.user.is_authenticated:
#         redirect('accounts:profile')
#     else:
#         redirect('accounts:qrcodeattendance')
#     return render(request, 'accounts/main.html')

def qrcodeattendance(request):    
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    return render(request, 'accounts/qrcodeattendance.html')


# @login_not_required
def login_views(request): 
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('accounts:profile')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login_form.html',{'form':form})
# i am not using login_required() because of using Middleware.py which does the same work as login_required()

def register(request):  
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.deploy()
            #login(request, user)
            return redirect('accounts:login')
        else:
            pass
    else:
        form = RegistrationForm()
    return render(request,'accounts/teacher_signup_form.html', {'form': form})


def student_signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = StudentSignUpForm(request.POST or None)
        if form.is_valid():
            user = form.deploy()
            #login(request, user)
            return redirect('accounts:login')
        else:
            pass
    else:
        form = StudentSignUpForm()

    return render(request,'accounts/student_reg_form.html',{'form':form})

class PasswordResetView(auth_views.PasswordResetView):
    from_email = 'admin@plavent.com'

def generate_uuid():
    uuid = os.urandom(12).hex()
    return uuid

def view_profile(request):  
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')

    POSITION_CHOICE = (
        (1,'Lecturer'),
        (2,'Asistant Professor'),
        (3,'Associate Professor'),
        (4,'Professor'),
    )
    user = request.user

    user_details = UserProfile.objects.get(user= user)
    
    courses = CourseCode.objects.filter(Q(teacher1=user)|Q(teacher2=user))
    repeat = set()
    for c in courses:
        repeat.add(c.session)
    
    #Checking! Is it logged in by a student or teacher
    check_user = StudentProfile.objects.filter(student_user= user)
    if check_user.exists() :
        return redirect('accounts:student_profile')

    class_teacher = TeacherProfile.objects.get(teacher_user=user) 
    present_sheet = class_teacher.class_presentsheet.all()  # QureySet of all present sheet of teacher
    
    # print(class_teacher.teacher_position)
    position = int(class_teacher.teacher_position)
    position = POSITION_CHOICE[position-1][position-1]


    """" classes held by others """
    last_five_present_sheets = PresentSheet.objects.order_by('-id')[:10]  
    last_five_sheets = list()
    for sheet in last_five_present_sheets:
        course = CourseCode.objects.get(course_code = sheet.select_course_code)
        teacher1 = TeacherProfile.objects.get(teacher_user=course.teacher1)
        all_t1= teacher1.class_presentsheet.all()
        teacher2 = TeacherProfile.objects.get(teacher_user=course.teacher2)
        all_t2= teacher2.class_presentsheet.all()

        total_course_student = StudentProfile.objects.filter(student_session=course.session).all().count()
        
        percentage = ((sheet.attend_user.all().count())/total_course_student)*100

        if sheet in all_t1:
            last_five_sheets.append((teacher1,sheet,percentage))
        elif sheet in all_t2:
            last_five_sheets.append((teacher2,sheet,percentage))

    if request.method == 'POST':
        course = request.POST.get('c')
        return redirect('accounts:course_present_sheet', course_code = course)

    context = {
        'user': user,
        'user_details':user_details,
        'courses': courses,
        'repeat': repeat,
        'present_sheet': present_sheet,
        'class_teacher': class_teacher,
        'position':position,
        'last_five_sheets':last_five_sheets,
    }
    return render(request, 'accounts/profile.html', context)

def view_student_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')

    return render(request, 'accounts/student_profile.html')

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')

    if request.method == 'POST':
        form = AdditionalInfoForm(request.POST or None, request.FILES, initial={'no': '123123'})
        if form.is_valid():
            instance = form.save(commit = False)
            profile = UserProfile.objects.get(user=request.user)
            profile.phone = instance.phone
            profile.image = instance.image
            profile.city = instance.city
            profile.country = instance.country
            # print(instance.phone)
            profile.save()
            return redirect('accounts:profile')
    else:
        form = AdditionalInfoForm()
    args = {'form': form}
    return render(request, 'accounts/edit_profile.html', args)


def view_session(request, slug):
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')        

    session = get_object_or_404(ClassSession, slug=slug)
    course_code = CourseCode.objects.filter(Q(session=session)&Q(Q(teacher1=request.user)|Q(teacher2=request.user)))
    selected_course_code = request.POST.get("course_code")
    course_student = StudentProfile.objects.filter(Q(student_session= session))

    print(selected_course_code)
    if request.method == 'POST':
        get_uuid = generate_uuid()
        get_course_code = request.POST.get('c')
        
        """" Creating present sheet """
        present_sheet_instance, created = PresentSheet.objects.get_or_create(  
        select_course_code= get_course_code,
        select_session = slug,
        random_url = get_uuid
        )
        present_sheet_instance.save()
        user = request.user
        teacher = TeacherProfile.objects.get(teacher_user=user)
        teacher.class_presentsheet.add(present_sheet_instance)
        
        """ Sending informations to QR code page """
        return redirect('accounts:view_qr_code',slug= slug, course_code=get_course_code, random_url= get_uuid)

    context = {
        'session': session,
        'course_code': course_code,
        'selected_course_code': selected_course_code,
        'course_student': course_student,
        # 'form': form, 
    }
    return render(request, 'accounts/session.html', context)

def present_sheet(request,random_url):
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')

    present_sheet = PresentSheet.objects.get(random_url=random_url) 
    student_user = present_sheet.attend_user.all()
  
    students = StudentProfile.objects.all().order_by('student_roll')

    session_students = list()
    for s in students:
        if s.student_session == str(present_sheet.select_session):
            session_students.append(s.student_user.username)

    attend_students = list()
    check = list()
    student_users = present_sheet.attend_user.all()
    for student in student_users :
        if student.username in session_students:
            attend_students.append(student.username)

    if request.method =="POST":
        return redirect('accounts:attendance_sheet_delete', random_url=random_url)         

    link = "http://127.0.0.1:8000/qrcodeattendance/profile/session/" +present_sheet.select_session+"/"+ present_sheet.select_course_code +"/qr_code_api"+"/"+ random_url
    context = {
        'link':link,
        'session_students':session_students,
        'attend_students':attend_students,
        'present_sheet': present_sheet,
        'student_user': student_user,
    }
    return render(request, 'accounts/present_sheet.html', context)

def attendance_sheet_delete(request, random_url):

    if request.method == "POST":
        if request.POST.get('c') == "yes":
            sheet = PresentSheet.objects.get(random_url=random_url)
            sheet.delete()
            messages.success(request, 'Your profile was updated.') 
            return redirect('accounts:profile')

        elif request.POST.get('c') == "no":
            return redirect('accounts:profile')
    
    context = {
        'random_url': random_url,
    }
    return render(request,'accounts/delete_present_sheet.html', context)


def course_present_sheet(request, course_code):
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')

    course =  CourseCode.objects.get(course_code= course_code)
    session = course.session
    students = StudentProfile.objects.all().order_by('student_roll')

    session_students = list()
    for s in students:
        if s.student_session == str(session):
            session_students.append(s.student_user.username)

    teacher = TeacherProfile.objects.get(teacher_user= request.user)
    all_present_sheets = teacher.class_presentsheet.all()
    course_present_sheets = list()
    for sheet in all_present_sheets:
        if sheet.select_course_code == str(course_code):
            course_present_sheets.append(sheet)

    attend_students = list()
    num_sheet = 0
    for sheet in course_present_sheets:
        num_sheet +=1
        check = list()
        date , rm =str(sheet.join_date).split('.') #date of each class 
        student_users = sheet.attend_user.all()
        for student in student_users:
            if student.username in session_students:
                check.append(student.username)
        attend_students.append([date,check])

    check = request.POST.get('c')
        
    if check is not None:
        return redirect('accounts:course_attendance_details_delete', course_code=course_code)
            


    if request.method == 'POST':
        student = request.POST.get('s')

        number_of_attend = 0
        for num in attend_students:
            if student in num[1]:
                number_of_attend +=1
        percentage = (number_of_attend/num_sheet)*100

        #storing percentage data
        user = User.objects.get(username=student)    
        student_user = StudentProfile.objects.get(student_user=user)
        user_session = ClassSession.objects.get(session= session)
        course_percentage, created = CoursePercentage.objects.get_or_create(student_user= user, course_code=course, session=user_session)
        if not created:
            course_percentage.percentage=percentage
            course_percentage.save()
        else:
            if percentage is None:
                percentage =0
            course_percentage.percentage = percentage
            course_percentage.save()
            
        return redirect('accounts:course_percentage', course_code=course_code,session=session, student=student)

    """ Paging the sheets """
    page = request.GET.get('page',1)
    paginator = Paginator(attend_students, 8)

    try:
        attend_students = paginator.page(page)
    except PageNotAnInteger:
        attend_students = paginator.page(1)
    except EmptyPage:
        attend_students = paginator.page(paginator.num_pages)

    print(attend_students.has_other_pages)

    context = {
        'session_students':session_students, 
        'attend_students':attend_students, 
        'course_code':course.course_code, 
    }

    return render(request,'accounts/course_present_details.html',context)

def course_attendance_details_delete(request, course_code):

    if request.method == "POST":
        if request.POST.get('c') == "yes":
            user = request.user
            teacher = TeacherProfile.objects.get(teacher_user=user)
            all_present_sheets = teacher.class_presentsheet.all()
            course_present_sheets = all_present_sheets.filter(select_course_code=course_code)
            
            sheets = course_present_sheets.all()
            for sheet in sheets:
                sheet.delete()
            messages.success(request, 'Your profile was updated.') 

            return redirect('accounts:profile')
        elif request.POST.get('c') == "no":
            return redirect('accounts:profile')
    context = {
        'course_code': course_code,
    }
    return render(request,'accounts/delete_all.html', context)





def view_qr_code(request, slug, course_code, random_url):
    if not request.user.is_authenticated:
        return redirect('accounts:qrcodeattendance')

    present_sheet = PresentSheet.objects.get(random_url= random_url)
    session_students = present_sheet.attend_user.all()

    attend_students = list()
    check = list()
    student_users = present_sheet.attend_user.all()
    for student in student_users :
        if student.username in session_students:
            attend_students.append(student.username)

    """ 
    Url making for QR code 
    Example: http://127.0.0.1:8000/profile/session/2015-16/ICE-1101/qr_code/5380c2eba11158223369c68a/
    slug, coursec_code, random_url are string
    """
    link = "http://127.0.0.1:8000/qrcodeattendance/profile/session/" + slug +"/"+ course_code +"/qr_code_api"+"/"+ random_url
    refresh_link = "http://127.0.0.1:8000/qrcodeattendance/profile/session/" + slug +"/"+ course_code +"/qr_code"+"/"+ random_url
    print(link)
    context = {
        'user': request.user,
        'link': link,
        'refresh_link':refresh_link,
        'course_code': course_code,
        'session': slug,   
        'session_students':session_students, 
    }           

    return render(request, 'accounts/qr_code_form.html', context )

def course_percentage(request, course_code, session, student):

    user = User.objects.get(username=student)

    course_percentage = CoursePercentage.objects.get(student_user=user)

    context = {
        'course_percentage': course_percentage,
    }
    return render(request, 'accounts/course_percentage.html', context)


""" ---- API VIEW ---- """    

class HelloApiView(APIView):
    """ Test API View """

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIView features """
        
        an_apiview = [
            'Uses HTTP methods as function(get, post, patch, put, delete',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message':'Heloo!', 'an_apiview': an_apiview})    

    def post(self, request):
        """ Create a hello message with out name """

        serializer = serializers.HelloSerializer(data = request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """ Handles updating an object. """

        return Response({'method':'put'})

    def patch(self, request, pk=None):
        """ Patch request, only update fields provied in the request. """

        return Response({'method':'patch'}) 
  
    def delete(self, request, pk=None):
        """ Deletes and object. """
        return Response({'method':'delete'})

class HelloViewSet(viewsets.ViewSet):
    """ Test API ViewSet """

    def list(self, request):
        """ Return a hello message. """

        a_viewset = [
            'Uses actions(list, creat, retrieve, update, partial_update',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})         

    def create(self, request):
        """ Create a new hello message. """

        serializer = serializers.HelloSerializer(data= request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Handles getting an object by its ID """
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """ Handles updating an object """
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """ Handles updating part of an object. """
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """ Handles removing an object """
        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles creating, creating and updating profile. """
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer

class StudentProfileViewSet(viewsets.ModelViewSet):
   
    queryset = StudentProfile.objects.all()
    serializer_class = serializers.StudentProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('student_session','student_user__username','student_user__email',)

class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an auth token """
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the obtainAuthToken APIView to validate and create a token """
        return ObtainAuthToken().post(request)

class AttendanceSheetView(APIView):

    def get(self, request, session, course_code, random_url):
        user = request.user  # student user request
        # presentsheet, created = PresentSheet.objects.get_or_create(attend_user=user)
        presentsheet = PresentSheet.objects.get(random_url = random_url)
        presentsheet.save()
        presentsheet.attend_user.add(user)

        return Response()    

class CoursePresentSheetViewSet(viewsets.ModelViewSet):
    queryset = PresentSheet.objects.all()
    serializer_class = serializers.CoursePresentSheetSerializer





