from django.db import models
from django.contrib import admin
# Create your models here.


class tempIMG(models.Model):
	img = models.ImageField(upload_to='faceRecog/static/facerecog/')#path
	def __str__(self):
		return self.img
admin.site.register(tempIMG)