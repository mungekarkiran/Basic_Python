from django.db import models

# Create your models here.

class NewUsers(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pwd1 = models.CharField(max_length=50)
    gender =  models.CharField(max_length=10)
    class Meta:
        # define table name
        db_table = 'NewUsers'
    
    # def __str__(self):
    #     return self.fname