from django.contrib import admin # type: ignore
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)