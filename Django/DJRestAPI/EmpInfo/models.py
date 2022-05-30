from django.db import models

# Create your models here.
class Emp(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    age = models.IntegerField()
    experience = models.FloatField()
    salary = models.FloatField()

    def __str__(self):
        return self.fname
    
    class Meta:
        # define table name
        db_table = 'Emp'
