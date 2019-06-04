from django.contrib import admin
from accounts.models import UserProfile,ClassSession, CourseCode, StudentProfile,TeacherProfile, PresentSheet, CoursePercentage


# Admin model
# Register your models here.
admin.site.register(UserProfile)

class ClassSessionAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('session',)}

admin.site.register(ClassSession)
admin.site.register(CourseCode)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(PresentSheet)
admin.site.register(CoursePercentage)
