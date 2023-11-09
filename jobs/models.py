from statistics import mode
from django.db import models
from django.utils import timezone
import math
from Employer.models import UserProfile
from django.urls import reverse
from ckeditor.fields import RichTextField
from org_photo.models import info as OrgModel

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps


status_choices = (
    ('approved','approved'),
    ('pending','pending'),
    ('declined','declined')
)
class Info(models.Model):
    
    jobs_slug = models.SlugField(max_length=1000, null=False, blank=False)
    job_title = models.CharField(max_length=1000, null=True, blank=True)
    meta_tag = models.CharField(max_length=1000, null=True, blank=True)
    job_location = models.CharField(max_length=500, null=True, blank=True)
    nationality = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=1000, null=True, blank=True)
    slug_cate = models.SlugField(max_length=1000, null=True, blank=True)
    slug_cpn = models.SlugField(max_length=1000, null=True, blank=True,allow_unicode=True)
    emp_type = models.CharField(max_length=300, null=True, blank=True)
    salary = models.CharField(max_length=500, null=True, blank=True)
    vacancy_number = models.CharField(max_length=500, null=True, blank=True)
    no_of_jobs = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    organzation = models.CharField(max_length=1000, null=True, blank=True)
    years_of_experience = models.CharField(max_length=500, null=True, blank=True)
    contract_duration = models.CharField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=500, null=True, blank=True)
    close_date = models.CharField(max_length=500, null=True, blank=True)
    About_description = RichTextField(null=True, blank=True)
    job_descriptions = RichTextField(null=True, blank=True)
    job_requirements = RichTextField(null=True, blank=True)
    submission_guidelines = RichTextField(null=True, blank=True)
    submission_email = models.CharField(max_length=500, null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    job_date = models.DateTimeField(default=timezone.now(), blank=True)
    activation_date = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length = 1000, null=True, blank=True)
    views = models.IntegerField(default=0)
    status = models.CharField(choices=status_choices,max_length=500, default='approved', blank=True, null=True)
    posted_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    org_photo = models.ForeignKey(OrgModel, on_delete=models.SET_NULL, null=True, blank=True)

        
    def approve_post(self):
        if not self.activation_date and self.status == 'approved':
            self.activation_date  = timezone.now()
            self.save()
        else:
            self.save()

    def __str__(self):
        if self.job_title:
            return self.job_title
        else:
            pass    
    def get_absolute_url(self):
        return reverse('category', kwargs={ "slug": self.slug_cate })

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.job_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


@receiver(pre_save, sender=Info)
def update_org_photo_id(sender, instance, **kwargs):
    OrgPhoto = apps.get_model('org_photo', 'info')  # Replace 'your_app_name' with your actual app name
    try:
        org_photo_id = OrgPhoto.objects.get(name=instance.organzation)
        instance.org_photo = org_photo_id
    except OrgPhoto.DoesNotExist:
        pass