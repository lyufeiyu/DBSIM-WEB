from django.db import models

# Create your models here.
class Resource(models.Model):    # test models
    name = models.CharField(max_length=200)
    value = models.FloatField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(models.Model):    # test models
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'user'
