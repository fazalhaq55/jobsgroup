from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

class info(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    vector_photo = models.ImageField(upload_to="vector_photos/", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    # Signal handler for post_save event of OrgPhoto model
@receiver(post_save, sender=info)
def update_jobs_info_org_photo(sender, instance, created, **kwargs):
    if created:
        JobsInfo = apps.get_model('jobs', 'Info')
        jobs_info = JobsInfo.objects.filter(organzation=instance.name)
        jobs_info.update(org_photo_id=instance.id)