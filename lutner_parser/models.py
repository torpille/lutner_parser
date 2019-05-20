from django.db import models

from django.utils import timezone

# Create your models here.

#Семейства моделей
class Section(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return  self.name

#Семейства моделей
class Category(models.Model):
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    def __str__(self):
        string = '{} {}'.format(self.name, self.section)
        return  string

#Производитель
class Brandname(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return  self.name

#Товары
class Product(models.Model):
    article = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=254, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    brandname = models.ForeignKey(Brandname, on_delete=models.PROTECT, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True, default=0)
    price = models.FloatField(blank=True, null=True, default=0)
    control_count = models.IntegerField(blank=True, null=True, default=0)
    control_check = models.BooleanField(default=False)
    def __str__(self):
        string = '{} {}'.format(self.brandname, self.article)
        return  string
        # return self.name

#Товары
class Statistics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()
    price = models.FloatField(blank=True, null=True)
    def __str__(self):
        string = '{} {} {} {}'.format(self.product, self.date, self.count, self.price)
        return  string

class Pagelink(models.Model):
    link = models.CharField(max_length=254, unique=True)
    def __str__(self):
        return  self.link
