from random import choice, choices
from django.db import models
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from django.utils import timezone
import math
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# OPP_CHOICES = (
#     ('Announcement', 'Announcement'),
#     ('Competition', 'Competition')
# )
Gender = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('male/female', 'Male/Female')  
)
LANG_CHOICES = (('toefl', 'TOEFL'),
                ('ielts', 'IELTS'),
                ('delf/dalf(french)', 'DELF/DALF(French)'),
                ('hsk(chines)', 'HSK(CHINES)'),
                ('pte_academic', 'PTE Academic'),
                ('cambridge qualification', 'Cambridge qualification'),
                ('dsh_german', 'DSH German'),
                ('cefr', 'CEFR'),
                ('duolingo', 'Duolingo'),
                ('japan_language(jlpt)', 'Japan Language(JLPT)'),
                ('tomor(turkish)', 'TOMOR(Turkish)'),
                ('other', 'Other'),
                ('not_required', 'Not required'))


MY_CHOICES = (('Announcement', 'Announcement'),
              ('Award/Grant', 'Award/Grant'),
              ('Competition', 'Competition'),
              ('Conference', 'Conference'),
              ('Courses', 'Courses'),
              ('Event', 'Event'),
              ('Fellowship', 'Fellowship'),
              ('Job', 'Job'),
              ('Leadership Program', 'Leadership Program'),
              ('Mentorship', 'Mentorship'),
              ('Online Courses', 'Online Courses'),
              ('Research', 'Research'),
              ('Residency Program', 'Residency Program'),
              ('Scholarship', 'Scholarship'),
              ('Short Program', 'Short Program'),
              ('Training', 'Training'),
              ('Volunteer Program', 'Volunteer Program'),
              ('Volunteer Compaign', 'Volunteer Compaign'),
              ('Volunteer Job', 'Volunteer Job'))

LEVEL_CHOICES = (('bachelor','Bachelor'),
                ('master','Master'),
                ('phd','PH.D'),
                ('school','School'),
                ('research','Research'),
                ('postdoc','PostDoc'),
                ('non_degree/short_program','Non-Degree /Short Program'))

MI_CHOICES = (('english','English'),
             ('chinese','Chinese'),
             ('japanese','Japanese'),
             ('korean','Korean'),
             ('turkish','Turkish'),
             ('slovaki','Slovaki'),
             ('romani','Romani'),
             ('german','German'),
             ('french','French'),
             ('spanish','Spanish'),
             ('arabic','Arabic'),
             ('persian','Persian'),
             ('russian','Russian'))
              
FUND_CHOICES = (('fully_funded','Fully Funded'),
               ('partially_founded','Partially Founded'),
               ('self_founded','Self Founded'))

               
class Detail(models.Model):
    scholarship_title = models.CharField(max_length=1000, null=True, blank=True)
    scho_meta = models.CharField(max_length=1000, null=True, blank=True)
    opp_desc = RichTextField(blank=True, null=True)
    email_address = models.CharField(max_length=500, null=True, blank=True)
    organization = models.CharField(max_length=500, null=True, blank=True)
    deadline = models.CharField(max_length=500, null=True, blank=True)
    opp_type =  MultiSelectField(choices=MY_CHOICES, null=True)
    opp_apply_type = models.CharField(max_length=500, null=True, blank=True)
    lang_requirements = MultiSelectField(choices=LANG_CHOICES, null=True)
    gender = models.CharField(max_length=50,choices=Gender, default='Male/Female', null=True, blank=True)
    level = MultiSelectField(choices=LEVEL_CHOICES, null=True)
    number_of_opp = models.CharField(max_length=50, null=True, blank=True)
    eligible_countries = RichTextField(blank=True, null=True)
    medium_of_instruction = MultiSelectField(choices=MI_CHOICES, null=True)
    field_of_stady = models.CharField(max_length=500, null=True, blank=True)
    funding_type = MultiSelectField(choices=FUND_CHOICES, null=True)
    duration = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    full_address = models.CharField(max_length=500, null=True, blank=True)
    scho_date = models.DateTimeField(default=timezone.now(), blank=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    opp_slug = models.SlugField(max_length=1000, blank=True)
    country_slug =models.SlugField(max_length=1000, blank=True)
    organization_slug = models.SlugField(max_length=1000, blank=True)
    views = models.IntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    
    def __str__(self):
        return self.scholarship_title


    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.scho_date

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

# this save function generate slug for scholarship
    def save(self, *args, **kwargs):
        if not self.opp_slug and self.country_slug and self.organization_slug:
            self.opp_slug = slugify(self.scholarship_title)
            self.country_slug = slugify(self.country)
            self.organization_slug = slugify(self.organization)
        super().save(*args, **kwargs)
        

# this will recive and will save the slug for scholarship
@receiver(pre_save, sender=Detail)
def detail_pre_save(sender, instance, **kwargs):
    instance.opp_slug = slugify(instance.scholarship_title)
    instance.country_slug = slugify(instance.country)
    instance.organization_slug = slugify(instance.organization)
# ***************************************************************************
    
    

