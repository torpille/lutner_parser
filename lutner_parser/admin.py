from django.contrib import admin
from .models import Section, Category, Brandname, Product, Statistics
# Register your models here.
admin.site.register(Section)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brandname)
admin.site.register(Statistics)