from django.contrib import admin

from .models import Category, Genre, MyUser, Title


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(MyUser)
admin.site.register(Title)
