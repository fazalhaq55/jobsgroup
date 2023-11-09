from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .forms import JobsForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from jobs.models import Info
# mail imports
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from Employer.models import UserProfile
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation, Now you can login to your account')
        return redirect('login')
    else:
        messages.error(request, 'Activation Link is invalid')   
    return redirect('home')

def login_view(request): 
    if request.method == "POST":
        Email = request.POST.get('email') # to get field data
        Password = request.POST.get('password')

        # return HttpResponse(password)
        user_object = UserProfile.objects.filter(email=Email).first()
        if user_object is None:
            messages.error(request, 'User not found.')
            return redirect('login')
        if user_object:
            if not user_object.is_active:
                messages.error(request, 'Email is not verified check your mail.')
                return redirect('login')

        if Email and Password:
            user = authenticate(email=Email, password=Password) # check the provided username is correct or not
            if user is not None: # Check if the user exist in database
                login(request, user) # Login is bult-in function which is imported from django.contrib.auth
                if request.POST.get('keep_signed_in'):
                # Set session cookie to expire in 30 days
                    request.session.set_expiry(30 * 24 * 60 * 60)
                return redirect('home')
            else:
                messages.error(request, 'Email address or Password is incorrect!')
        else:
            messages.error(request, 'Please fill out the fields')

    return render(request, 'Employer/login.html')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate Your Account'
    message = render_to_string('Employer/activate_user_account_email.html', {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(request, f'Dear <b>{user.first_name}</b>, please go to your email <b>{to_email}</b> inbox and click on the verification button to confirm and complete the registration.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')

def register(request):
           
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = CreateUserForm() # Means when the form is empty show user the form again

    return render(request, 'Employer/register.html', {'form':form})

@login_required(login_url='login')
def home(request):
    
    jobs_posted = Info.objects.filter(is_expired=False, posted_by = request.user).count
    jobs_pending = Info.objects.filter(is_expired=False, status='pending', posted_by = request.user).count
    jobs_approved = Info.objects.filter(is_expired=False, status='approved', posted_by = request.user).count
    jobs_declined = Info.objects.filter(is_expired=False, status='declined', posted_by = request.user).count
    
    
    context = {
        'jobs_posted':jobs_posted, 
        'jobs_pending':jobs_pending,
        'jobs_approved': jobs_approved,
        'jobs_declined':jobs_declined
        
    }
    return render(request, 'Employer/home.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_job(request):
    if request.user.is_superuser:
        jobs = Info.objects.filter(status='pending')
    else:
        jobs = Info.objects.filter(posted_by=request.user)

    user_org = request.user.company_name
    organization_info = request.user.about_company

    form = JobsForm()
    if request.method == 'POST':
        form = JobsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) # means save the form but dont commit and create object

            job_locations = form.cleaned_data.get('job_location') # to get job location data
            job_title = form.cleaned_data.get('job_title')
            category = form.cleaned_data.get('category')
            organization = form.cleaned_data.get('organzation')
            nationality = form.cleaned_data.get('nationality')
            emp_type = form.cleaned_data.get('emp_type')
            no_of_jobs = form.cleaned_data.get('no_of_jobs')
            gender = form.cleaned_data.get('gender')
            close_date = form.cleaned_data.get('close_date')
            submission_guidelines = form.cleaned_data.get('submission_guidelines')

            if not job_title or not job_locations or not nationality or not submission_guidelines or not emp_type or not category or not no_of_jobs or not organization or not gender or not close_date:
                messages.error(request, 'Please fill out the required fields.')
                return redirect('add_job')
            else:

                
                job_locations = ', '.join(job_locations) # split the array using , 
                meta_tag = job_title
                slug_cate = slugify(category)
                slug_cpn = slugify(organization)
                jobs_slug = slugify(job_title)

                instance.job_location = job_locations # save the splited data into job_location field
                instance.meta_tag = meta_tag
                instance.slug_cate = slug_cate
                instance.slug_cpn = slug_cpn
                instance.jobs_slug = jobs_slug
                
                if not request.user.is_superuser: # check if the logged in user is super or not
                    instance.status = 'pending' # make the status to false because the user is not superuser
                    instance.posted_by = request.user
                instance.save()
                messages.success(request, 'The job has been posted successfully. Please wait for approval')
                return redirect('add_job')
    else:
        data_to_forms = {
            'organzation':request.user.company_name,
            'About_description':request.user.about_company} # passing the value to organization field ({{ forms.organization }}) in add_job.html

        form = JobsForm() 
        form = JobsForm(initial=data_to_forms) 
        
    context = {
        'jobs':jobs,
        'user_org':user_org,
        'organization_info':organization_info,
        'form':form
    }
    return render(request, 'Employer/add_job.html',context)
    

# @login_required(login_url='login')
# def save_job(request):
    # if request.method == "POST":
    #     job_title = request.POST.get('job_title')
    #     job_locations = request.POST.getlist('job_location')
    #     nationality = request.POST.get('nationality')
    #     emp_type = request.POST.get('emp_type')
    #     category = request.POST.get('category')
    #     vacancy_number = request.POST.get('vacancy_number')
    #     salary = request.POST.get('salary')
    #     no_of_jobs = request.POST.get('no_of_jobs')
    #     city = request.POST.get('city')
    #     organization = request.POST.get('organization')
    #     years_of_experience = request.POST.get('years_of_experience')
    #     contract_duration = request.POST.get('contract_duration')
    #     gender = request.POST.get('gender')
    #     education = request.POST.get('education')
    #     close_date = request.POST.get('close_date')
    #     about_desc = request.POST.get('about_desc')
    #     job_desc = request.POST.get('job_desc')
    #     job_requirements = request.POST.get('job_requirements')
    #     submission_guidlines = request.POST.get('submission_guidlines')
    #     submission_email = request.POST.get('submission_email')

    #     if not job_title or not job_locations or not nationality or not emp_type or not category or not no_of_jobs or not organization or not gender or not close_date:
    #         messages.error(request, 'Please fill out the required fields.')
    #         return redirect('add_job')
    #     else:
    #         jobs_slug = slugify(job_title)
    #         slug_cate = slugify(category)
    #         slug_cpn = slugify(organization)

    #         job_location = ','.join(job_locations)
            
    #         JobsInfo = Info(job_title = job_title,meta_tag=job_title,jobs_slug=jobs_slug,slug_cate=slug_cate,slug_cpn=slug_cpn, job_location=job_location, nationality=nationality, emp_type=emp_type, category=category, vacancy_number=vacancy_number
    #                         ,salary=salary,no_of_jobs=no_of_jobs, city=city, organzation =organization, years_of_experience=years_of_experience, contract_duration=contract_duration, 
    #                         gender=gender, education=education,close_date=close_date,About_description=about_desc, job_descriptions=job_desc, job_requirements=job_requirements,
    #                         submission_guidelines=submission_guidlines, submission_email=submission_email, )
                
    #         if not request.user.is_superuser: # check if the logged in user is super or not
    #                 JobsInfo.status = 'pending' # make the status to false because the user is not superuser
    #                 JobsInfo.posted_by = request.user
    #         JobsInfo.save()
    #         messages.success(request, 'The job has been posted successfully. Please wait for approval')
    #         return redirect('add_job')

@login_required(login_url='login')
def settings(request):
    user = request.user
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreateUserForm(instance=user)
    return render(request, 'Employer/user_settings.html', {'form': form})

@login_required(login_url='login')
def job_listing(request, id):

    jobs = Info.objects.filter(posted_by=id)
    return render(request, 'Employer/jobs_listing.html', {'jobs':jobs})
    

@login_required(login_url='login')
def edit_job(request, id):
    job = get_object_or_404(Info, id=id)
   
    if request.method == 'POST':
        form = JobsForm(request.POST, instance=job)
        if form.is_valid():
            instance = form.save(commit=False) # means save the form but dont commit and create object

            job_locations = form.cleaned_data.get('job_location') # to get job location data
            job_title = form.cleaned_data.get('job_title')
            category = form.cleaned_data.get('category')
            organization = form.cleaned_data.get('organzation')
            nationality = form.cleaned_data.get('nationality')
            emp_type = form.cleaned_data.get('emp_type')
            no_of_jobs = form.cleaned_data.get('no_of_jobs')
            gender = form.cleaned_data.get('gender')
            close_date = form.cleaned_data.get('close_date')
            submission_guidelines = form.cleaned_data.get('submission_guidelines')

            if not job_title or not job_locations or not nationality or not submission_guidelines or not emp_type or not category or not no_of_jobs or not organization or not gender or not close_date:
                messages.error(request, 'Please fill out the required fields.')
                return redirect('edit', pk=id)
            else:

                job_locations = ', '.join(job_locations) # split the array using , 
                meta_tag = job_title
                slug_cate = slugify(category)
                slug_cpn = slugify(organization)
                jobs_slug = slugify(job_title)

                instance.job_location = job_locations # save the splited data into job_location field
                instance.meta_tag = meta_tag
                instance.slug_cate = slug_cate
                instance.slug_cpn = slug_cpn
                instance.jobs_slug = jobs_slug

                if not request.user.is_superuser: # check if the logged in user is super or not
                    instance.status = 'pending' # make the status to false because the user is not superuser
                    instance.posted_by = request.user
                instance.save()
                messages.success(request, 'The job has been posted successfully. Please wait for approval')
                return redirect('edit',id=id)
    else:
        # organzation = {'organzation':request.user.company_name} # passing the value to organization field ({{ forms.organization }}) in add_job.html
        form = JobsForm(instance=job) 
        # form = JobsForm(initial=organzation) 

    return render(request, 'Employer/edit_job.html', {'form': form})
    
def password_reset_request(request):
    if request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            email = password_form.cleaned_data.get('email')
            user_email = UserProfile.objects.filter(Q(email=email))
            if user_email.exists():
                for user in user_email:
                   
                    mail_subject = 'Password Reset Request'
                    message = render_to_string('Employer/password_reset_request_text.html', {
                        'email': user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Wazifaha.org',
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https'
                    })
                    email = EmailMessage(mail_subject, message, to=[user.email])
                    email.content_subtype = "html"

                    try:
                        email.send() # fail_silently means when the email is wrong the system wont crush
                    except:
                        return HttpResponse('invalid header')
                    return redirect('password_reset_done')
            else:
                messages.error(request, 'Email not registered. Please check email address or create new account')
    else:
        password_form = PasswordResetForm

    context = {
        'password_form':password_form
    }    
    return render(request, 'Employer/password_reset.html', context)




# def password_reset_request(request):
#     if request.method == "POST":
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             email = password_form.cleaned_data.get('email')
#             user_email = UserProfile.objects.filter(Q(email=email))
#             if user_email.exists():
#                 for user in user_email:
#                     subject = "Password Request"
#                     email_template_name = 'Employer/Password_message.txt'
#                     parameters = {
#                         'email':user.email,
#                         'domain': 'wazifaha.org',
#                         'site_name': 'Wazifaha.org',
#                         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token': default_token_generator.make_token(user),
#                         'protocol' : 'https',
#                     }
#                     email = render_to_string(email_template_name, parameters) # we passing up values to email 
#                     try:
#                         send_mail(subject, email, '', [user.email], fail_silently=False) # fail_silently means when the email is wrong the system wont crush
#                     except:
#                         return HttpResponse('invalid header')
#                     return redirect('password_reset_done')
#             else:
#                 messages.error(request, 'Email not registered. Please check email address or create new account')
#     else:
#         password_form = PasswordResetForm

#     context = {
#         'password_form':password_form
#     }    
#     return render(request, 'Employer/password_reset.html', context)