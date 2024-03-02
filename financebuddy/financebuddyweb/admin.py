from django.contrib import admin
from .models import Category, Budget, Source
# Register your models here.
admin.site.register(Category)
admin.site.register(Source)
admin.site.register(Budget)