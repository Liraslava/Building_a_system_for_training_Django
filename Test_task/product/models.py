from django.db import models
from django.conf import settings
from django.contrib.auth.models import User  # We use the standard Django user model
from .serializers import LessonSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#  creating a user entity
# class User(models.Model):
#     name = models.CharField(blank=False)


# creating a product entity
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# creating a separate model for managing access to the product
class ProductAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Access to {self.product.name} for {self.user.username}"


# creating a lesson entity
class Lesson(models.Model):
    title = models.CharField(max_length=255, blank=False)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()
    products = models.ManyToManyField('Product', related_name='lessons')

    def __str__(self):
        return self.title

# creating a model for tracking browsing
class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)  # Status "Viewed"/"Not viewed"
    watched_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Viewing percentage
    timestamp = models.DateTimeField(auto_now=True)



# creating a lesson and adding it to the product
product = Product.objects.get(pk=1)  # get the product
lesson = Lesson.objects.create(title="Урок 1", video_link="https://", duration_seconds=120)
lesson.products.add(product)  # add a product to the lesson