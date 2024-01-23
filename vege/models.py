from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #this is used so as to delete the recipes if that user acc is deleted
    recipe_name = models.CharField(max_length=200)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to="recipe")