from django.db import models

# Create your models here.
class myLang(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return self.name
    

