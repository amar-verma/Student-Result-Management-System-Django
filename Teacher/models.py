from django.db import models

# Create your models here.
class teacher(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    div = models.CharField(max_length=5)
    std = models.IntegerField()
    board = models.CharField(max_length=50)

    def __str__(self):
        return self.username