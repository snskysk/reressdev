from django.contrib import admin

# Register your models here.
from .models import studentInfo, subjectInfo


admin.site.register(studentInfo)
admin.site.register(subjectInfo)
admin.site.register(food_pool)

from django.contrib import admin
from .models import Post

admin.site.register(Post)
