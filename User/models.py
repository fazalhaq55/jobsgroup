from django.db import models

class Message(models.Model):
    user_name = models.CharField(max_length=250, null=True, blank=True)
    user_email = models.CharField(max_length=250, null=True, blank=True)
    user_message = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.user_message
