from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from jobs.models import Info
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField

class CreateUserForm(UserCreationForm):
    
    COMPANY_TYPE_CHOICES = [
        ('employer_private_sector','Employer (Private Sector)'),
        ('employer_public_sector','Employer (Public Sector)'),
        ('non_proft_organization','Non-Profit Organization'),
        ('recruitment_agency','Recruitment Agency')
    ]

    first_name = forms.CharField(required=True, error_messages={'required': 'The first name is required'}) 
    company_name = forms.CharField(required=True, error_messages={'required': 'The company name is required'}) 
    contact_number = forms.IntegerField(required=True, error_messages={'required': 'The contact number is required'}) 
    company_type = forms.ChoiceField(choices=COMPANY_TYPE_CHOICES, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    country = CountryField().formfield(required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['autocomplete'] = 'first_name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['autocomplete'] = 'country'
        self.fields['company_type'].widget.attrs['class'] = 'form-control'
        self.fields['company_name'].widget.attrs['class'] = 'form-control'
        self.fields['contact_number'].widget.attrs['class'] = 'form-control'
        self.fields['about_company'].widget.attrs['class'] = 'form-control'
        self.fields['company_image'].widget.attrs['class'] = 'form-control'
        

    class Meta:
        model = UserProfile
        country = CountryField().formfield() # country is select field so we are passing that like this
        fields = ['first_name','last_name', 'email', 'password1', 'password2','country','company_type','company_name'
                  ,'contact_number','about_company','company_image']
        
# Here we get Info Model and we are creating ModelForm using django default forms and we are passing model fields using fields array
class JobsForm(forms.ModelForm):
    
    Jobs_location_choices = [
        ('Badakhshan','Badakhshan'),
        ('Badghis','Badghis'),
        ('Baghlan','Baghlan'),
        ('Balkh','Balkh'),
        ('Bamyan','Bamyan'),
        ('Farah','Farah'),
        ('Faryab','Faryab'),
        ('Ghazni','Ghazni'),
        ('Ghor','Ghor'),
        ('Helmand','Helmand'),
        ('Herat','Herat'),
        ('Jawzjan','Jawzjan'),
        ('Kabul','Kabul'),
        ('Kandahar','Kandahar'),
        ('Kapisa','Kapisa'),
        ('Khost','Khost'),
        ('Kunar','Kunar'),
        ('Kunduz','Kunduz'),
        ('Laghman','Laghman'),
        ('Maidan Wardak','Maidan Wardak'),
        ('Nangarhar','Nangarhar'),
        ('Nangarhar','Nangarhar'),
        ('Nimruz','Nimruz'),
        ('Nuristan','Nuristan'),
        ('Oruzgan','Oruzgan'),
        ('Paktia','Paktia'),
        ('Paktika','Paktika'),
        ('Panjshir','Panjshir'),
        ('Parwan','Parwan'),
        ('Samangan','Samangan'),
        ('Sar-e Pol','Sar-e Pol'),
        ('Takhar','Takhar'),
        ('Zabul','Zabul'),
    ]
    nationality_choices = [
        ('National','National'),
        ('International', 'International'),
        ('National/International','National/International')
    ]

    emp_type_choices = [
        ('Full Time','Full Time'),
        ('Part Time','Part Time'),
        ('Freelance','Freelance')
    ]

    gender_choices = [
        ('Male/Female','Male/Female'),
        ('Male','Male'),
        ('Female','Female')
    ]

    #in the top we define fields types that it should be Checkbox or etc 
    job_location = forms.MultipleChoiceField(choices=Jobs_location_choices, widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    nationality = forms.ChoiceField(choices=nationality_choices, widget=forms.Select(attrs={'class':'form-control'}))
    emp_type = forms.ChoiceField(choices=emp_type_choices, widget=forms.Select(attrs={'class':'form-control'}))
    no_of_jobs = forms.IntegerField(error_messages={'invalid':'Please Enter a valid Integer'})
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class':'form-control'}))
    close_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
     # in the follwing we define the attributes of fields class, id and more
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['job_title'].widget.attrs['class'] = 'form-control'
        self.fields['emp_type'].widget.attrs['class'] = 'form-control'
        self.fields['vacancy_number'].widget.attrs['class'] = 'form-control'
        self.fields['salary'].widget.attrs['class'] = 'form-control'
        self.fields['no_of_jobs'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['job_location'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class']='form-control'
        self.fields['organzation'].widget.attrs['class']='form-control'
        self.fields['contract_duration'].widget.attrs['class']='form-control'
        self.fields['education'].widget.attrs['class']='form-control'
        self.fields['close_date'].widget.attrs['class']='form-control'
        self.fields['years_of_experience'].widget.attrs['class']='form-control'
        self.fields['submission_email'].widget.attrs['class']='form-control'

    # job_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})) # to add place holder
     # make job_location field the choice field and add class to it
    class Meta:
        model = Info
        fields = ['job_title','emp_type','vacancy_number','gender','submission_email','About_description', 'salary','no_of_jobs','category',
                  'job_location','city','job_location','organzation','contract_duration','education','close_date','years_of_experience',
                  'job_descriptions','job_requirements','submission_guidelines','nationality']
