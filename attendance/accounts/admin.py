from django.contrib import admin
from accounts.models import UserProfile,ClassSession, CourseCode, StudentProfile,TeacherProfile, PresentSheet, CoursePercentage


# Admin model
# Register your models here.
admin.site.register(UserProfile)

class ClassSessionAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('session',)}

class CourseCodeAdmin(admin.ModelAdmin):
	search_fields = ('course_code',)

class StudeneProfileAdmin(admin.ModelAdmin):
	search_fields = ('student_id','student_user__first_name','student_user__last_name','student_user__username','student_user__email')
class PresentSheetAdmin(admin.ModelAdmin):
	search_fields = ('join_date',)
class CoursePercentageAdmin(admin.ModelAdmin):
	search_fields = ('student_user__first_name','student_user__last_name','student_user__username','student_user__email')

admin.site.register(ClassSession)
admin.site.register(CourseCode, CourseCodeAdmin)
admin.site.register(StudentProfile, StudeneProfileAdmin)
admin.site.register(TeacherProfile)
admin.site.register(PresentSheet, PresentSheetAdmin)
admin.site.register(CoursePercentage, CoursePercentageAdmin)
