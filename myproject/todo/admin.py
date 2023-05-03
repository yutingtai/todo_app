from django.contrib import admin
from .models import UserDbModel,TodoDbModel

# Register your models here.
admin.site.register(UserDbModel)
admin.site.register(TodoDbModel)
