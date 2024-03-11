from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Info
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
import datetime
from django.db.models import Q
# from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator
from application.models import Form
import re
from org_photo.models import info as OrgModel
from prov_photo.models import info as ProvModel

def view(request):
    return render(request, 'pages/comming_soon.html')
def jobs(request):
    
    myDate = datetime.date.today()
    today = myDate.strftime("%Y-%m-%d")
   
    jobs = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    categories = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:30]
    org = Info.objects.filter(is_expired=False, status = 'approved').values('organzation','slug_cpn','posted_by').annotate(total = Count('slug_cpn')).order_by('-total')[:30]
    
    jobs_count = Info.objects.filter(is_expired=False, status = 'approved').count # to count all jobs
    
    paginator = Paginator(jobs, 8)
    page = request.GET.get('page')
    try:
        paged_jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_jobs = paginator.get_page(page)

    females_only = Info.objects.all().filter(is_expired=False, gender='Female',status = 'approved')
    ExpiringJobs = Info.objects.filter(Q(close_date=today), status = 'approved')
    featured_cities = Info.objects.filter(is_expired=False,status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')[:4]
    
    org_photos = OrgModel.objects.all()
    prov_photos = ProvModel.objects.all()
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
    count_companies = Info.objects.filter(is_expired=False, status = 'approved').values('slug_cpn').annotate(total = Count('slug_cpn')).count 
    

    cities = Info.objects.filter(is_expired=False, status = 'approved').values('city','city_slug').annotate(total = Count('city')).order_by('-total')
    company_industry = Info.objects.filter(is_expired=False, status = 'approved').values('company_industry','company_industry_slug').annotate(total = Count('company_industry')).order_by('-total')
    company_type = Info.objects.filter(is_expired=False, status = 'approved').values('company_type','company_type_slug').annotate(total = Count('company_type')).order_by('-total')
    emp_type = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    

    jobs_dict = {
        'jobs': paged_jobs,
        'jobs_count': jobs_count,
        'locations': locations,
        'categories':categories,
        'organization': org,
        'females_only' : females_only,
        'ExpiringJobs': ExpiringJobs,
        'featured_cities': featured_cities,
        'org_photos': org_photos,
        'prov_photos':prov_photos,
        'categories_for_search':categories_for_search,
        'count_companies':count_companies,
        'cities': cities,
        'company_industry':company_industry,
        'company_type':company_type,
        'emp_type':emp_type
    }
    return render(request, 'jobs/jobs.html', jobs_dict)

def job_details(request, id, slug):
    job = Info.objects.filter(jobs_slug=slug, id = id , status = 'approved').first()
   
    similiar_jobs = Info.objects.filter(category = job.category, is_expired=False, status = 'approved').order_by('-activation_date','-id')[:10]
    org_photos = OrgModel.objects.all()

    locations = Info.objects.filter(is_expired=False, status='approved').values('city').annotate(total=Count('city')).order_by('-total')
    emp_type = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
    
    
    # TO GET IP OF USER AND COUNT THE VISITS
    # def get_ip(request):
    #     address = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if address:
    #         ip = address.split(',')[-1].strip()
    #     else:
    #         ip = address.META.get('REMOTE_ADDR')
    #     return ip

    # ip = get_ip(request)
    # job.views = ip
    # result = Info.objects.filter(views__icontains=ip)
    # if len(result) == 1:
    #     print('user exits')
    # elif len(result) > 1:
    #     print('user exists more..')
    # else:
    #     job.save()
    #     print('user is unique')
    # count = Info.objects.all().values('views').annotate(total=Count('views'))
    # print('total views is ', count)

    if job:
        
        job.views = job.views + int(1)
        job.save()

        context = {
            'job': job,
            'similiar_jobs': similiar_jobs,
            'org_photos':org_photos,
            'locations':locations,
            'categories_for_search':categories_for_search,
            'emp_type':emp_type
        }

        return render(request, 'jobs/jobs_details.html', context)
    else:
        return render(request, 'jobs/404.html')


def category(request, slug):
    myDate = datetime.date.today()
    today = myDate.strftime("%Y-%m-%d")
    

    org = Info.objects.filter(is_expired=False, status = 'approved').values('organzation','slug_cpn','posted_by').annotate(total = Count('slug_cpn')).order_by('-total')[:30]
    
    jobs_founded = Info.objects.filter(slug_cate = slug, is_expired=False, status = 'approved').order_by('-activation_date','-id')
    categories = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:30]
    
    
    count_rows = Info.objects.filter(slug_cate = slug, is_expired=False, status = 'approved').count()
    jobs_count = Info.objects.all().filter(is_expired=False, status = 'approved').count
    category_name = Info.objects.filter(slug_cate = slug, is_expired=False, status = 'approved').values('category').first
    paginator = Paginator(jobs_founded, 15)
    page = request.GET.get('page')
    try:
        paged_jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_jobs = paginator.get_page(page)

    females_only = Info.objects.all().filter(is_expired=False, gender='Female', status = 'approved')
    ExpiringJobs = Info.objects.filter(Q(close_date=today), status = 'approved')
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    org_photos = OrgModel.objects.all()
    
    context = {
        'jobs_founded': paged_jobs,
        'count_rows': count_rows,
        'category': category_name,
        'jobs_count': jobs_count,
        'categories':categories,
        'locations': locations,
        'females_only' : females_only,
        'ExpiringJobs': ExpiringJobs,
        'org_photos':org_photos,
        'organization':org
    }
    return render(request, 'jobs/view_category_jobs.html', context)

def application_form(request):
    data = Form.objects.all()

    context = {
        'data': data,
    }
    return render(request, 'jobs/application_forms.html', context)

def apply(request,id, slug):
    job = Info.objects.filter(jobs_slug=slug, id = id).first()

    org_photos = OrgModel.objects.all()
    
    
    context = {
            'job': job,
            'org_photos':org_photos
        }   
    reg_ex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    matched = re.findall(reg_ex, job.submission_email)
    is_match = bool(matched)
    
    def listToString(s): 
    
        # initialize an empty string
        str1 = " " 
        
        # return string  
        return (str1.join(s))

    link = listToString(matched)
    if link:
         return HttpResponseRedirect(link)
    else:             
        return render(request, 'jobs/apply.html',context)
    