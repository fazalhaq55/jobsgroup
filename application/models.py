from django.db import models

class Form(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True,blank=True)
    company = models.CharField(max_length=1000, null=True, blank=True)
    filename = models.FileField()

    def __str__(self):
        return self.title
    