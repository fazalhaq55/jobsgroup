from django.db import models

class info(models.Model):
    name = models.CharField(max_length=500)
    photo = models.ImageField(upload_to="prov_photo")
    
    def __str__(self):
        return self.name