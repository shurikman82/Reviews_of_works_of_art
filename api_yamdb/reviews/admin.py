from django.contrib import admin

from .models import Category, Genre, CustomUser, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'genre', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(CustomUser)
admin.site.register(Title, TitleAdmin)
