from django.db import models

# Create your models here.
class msg(models.Model):
	user_name = models.TextField(max_length=20)
	description=models.TextField(max_length=200)
