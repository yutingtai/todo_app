from django.db import models


# Create your models here.
class UserDbModel(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class TodoDbModel(models.Model):
    TODO_STATUS = [
        ("InProgress", "InProgress"),
        ("Done", "Done"),
        ("NotStarted", "NotStarted"),
    ]
    status = models.CharField(max_length=10, choices=TODO_STATUS, default="NotStarted")
    title = models.CharField(max_length=100)
    user = models.ForeignKey(UserDbModel, on_delete=models.CASCADE)
