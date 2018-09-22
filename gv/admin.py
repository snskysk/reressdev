from django.contrib import admin

# Register your models here.
from .models import studentInfo, subjectInfo


admin.site.register(studentInfo)
admin.site.register(subjectInfo)
