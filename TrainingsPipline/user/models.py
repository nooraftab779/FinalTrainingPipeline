from django.db import models


# Create your models here.
class User(models.Model):
    User_id = models.AutoField
    User_name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=100, default="", null=False)

    def __str__(self):
        return self.User_name

    empAuth_objects = models.Manager()
