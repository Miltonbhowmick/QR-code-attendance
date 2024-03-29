from django.contrib import admin
from accounts.models import UserProfile,ClassSession, CourseCode, StudentProfile,TeacherProfile, PresentSheet, CoursePercentage


# Admin model
# Register your models here.
admin.site.register(UserProfile)

class ClassSessionAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('session',)}
	search_fields = ('session',)

class CourseCodeAdmin(admin.ModelAdmin):
	search_fields = ('course_code',)

class StudentProfileAdmin(admin.ModelAdmin):
	search_fields = ('student_user__username','student_id',)

class PresentSheetAdmin(admin.ModelAdmin):
	search_fields = ('joint_date','select_session','select_course_code',)

class CoursePercentageAdmin(admin.ModelAdmin):
	search_fields = ('student_user__username','student_user__email','student_user__first_name','student_user__last_name',)

admin.site.register(ClassSession,ClassSessionAdmin)
admin.site.register(CourseCode,CourseCodeAdmin)
admin.site.register(StudentProfile,StudentProfileAdmin)
admin.site.register(TeacherProfile)
admin.site.register(PresentSheet,PresentSheetAdmin)
admin.site.register(CoursePercentage,CoursePercentageAdmin)
