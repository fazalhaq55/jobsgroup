from django.shortcuts import render, get_object_or_404
from jobs.models import Info
from django.db.models import Count
from django.db.models import Q
import datetime
from Employer.models import UserProfile
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Sum
from django.db.models import IntegerField
from django.db.models.functions import Cast
from org_photo.models import info as OrgModel
from prov_photo.models import info as ProvModel
from django.http import JsonResponse, HttpResponse

def view(request):
    return render(request, 'pages/comming_soon.html')
    
def index(request):
    
    # DELETE THOSE RECORDS WHICH IS > THAN NOW DATE

    myDate = datetime.date.today()
    today = myDate.strftime("%Y-%m-%d")
 
    UserObj = UserProfile.objects.all()        
  
    # END DELETING
    org = Info.objects.filter(is_expired=False, status = 'approved').values('organzation','slug_cpn','posted_by').annotate(total = Count('slug_cpn')).order_by('-total')[:30]
    jobs = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')
    org_photos = OrgModel.objects.all()
    prov_photos = ProvModel.objects.all()
    
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
   
    paginator = Paginator(jobs, 8)
    page = request.GET.get('page')
    try:
        paged_jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_jobs = paginator.get_page(page)

    featured_companies = Info.objects.filter(is_expired=False, status = 'approved').values('organzation','slug_cpn','posted_by').annotate(total = Count('organzation')).order_by('-total')[:10]

    jobs_count = Info.objects.all().filter(is_expired=False, status = 'approved').count()
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
    categories = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:30]
    
    count_companies = Info.objects.filter(is_expired=False, status = 'approved').values('slug_cpn').annotate(total = Count('slug_cpn')).count 



    cities = Info.objects.filter(is_expired=False, status = 'approved').values('city','city_slug').annotate(total = Count('city')).order_by('-total')
    company_industry = Info.objects.filter(is_expired=False, status = 'approved').values('company_industry','company_industry_slug').annotate(total = Count('company_industry')).order_by('-total')
    company_type = Info.objects.filter(is_expired=False, status = 'approved').values('company_type','company_type_slug').annotate(total = Count('company_type')).order_by('-total')
    emp_type = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    
    context = {
        'categories': categories,
        'jobs_count': jobs_count,
        'jobs_founded': paged_jobs,
        'locations': locations,
        'organization': org,
        'featured_companies': featured_companies,
        'org_photos':org_photos,
        'prov_photos':prov_photos,
        'categories_for_search':categories_for_search,
        'UserObj':UserObj,
        'count_companies':count_companies,
        'cities': cities,
        'company_industry':company_industry,
        'company_type':company_type,
        'emp_type':emp_type
    }
    
    # it will get category, slug_cate columns, will group by that with category, will order by total and will take just 8 records

    # categories = job_info.objects.filter(category__gt=5).values('category').annotate(total=Count('category')).order_by('category')
    # it will filter the categories which is gt or greather than 5 and group by the category and store the counted in total

    # Returns the number of entries whose headline contains 'Lennon'
    # Entry.objects.filter(headline__contains='Lennon').count()
    
  

    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html') 

def search(request):
   
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    org_photos = OrgModel.objects.all()
    
   
    query_set_list = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')
    count_rowss = Info.objects.all().filter(is_expired=False, status = 'approved').count()
    
    what = request.GET['what']
    where = request.GET['where']
    category = request.GET['category']
    emp_type = request.GET['emp_type']

    category_name = Info.objects.filter(slug_cate = category, is_expired=False, status = 'approved').values('category').first
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
    emp_type_ = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
   
    #what
    if 'what' in request.GET:
        what = request.GET['what']
        if what:
            query_set_list = query_set_list.filter(job_title__icontains=what)
            count_rows = query_set_list.filter(job_title__icontains=what).count()
        else:
            query_set_list = query_set_list
            count_rows = count_rowss
    if 'where' in request.GET:
        where = request.GET['where']
        if where:
            query_set_list = query_set_list.filter(job_location__iexact=where)
            count_rows = query_set_list.filter(job_location__iexact=where).count()
        else:
            query_set_list = query_set_list

    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            query_set_list = query_set_list.filter(slug_cate__iexact=category)
            count_rows = query_set_list.filter(slug_cate__iexact=category).count()
        else:
            query_set_list = query_set_list
    
    if 'emp_type' in request.GET:
        emp_type = request.GET['emp_type']
        if emp_type:
            query_set_list = query_set_list.filter(emp_type__iexact=emp_type)
            count_rows = query_set_list.filter(emp_type__iexact=emp_type).count()
        else:
            query_set_list = query_set_list
    
    context = {
        'categories_for_search':categories_for_search,
        'jobs_founded': query_set_list,
        'what_keyword': what,
        'where_keyword': where,
        'count_rows': count_rows,
        'locations' : locations,
        'org_photos':org_photos,
        'category_name':category_name,
        'emp_type':emp_type,
        'emp_type_':emp_type_
    }
    return render(request, 'pages/search.html', context)

def searchJob(request, where):
    
    
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
   
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    
    query_set_list = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')
    org_photos = OrgModel.objects.all()
    emp_type_ = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
   
    if where:
        query_set_list = query_set_list.filter(job_location__iexact=where)
        count_rows = query_set_list.filter(job_location__iexact=where).count()
        
    paginator = Paginator(query_set_list, 12)
    page = request.GET.get('page')
    try:
        paged_jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_jobs = paginator.get_page(page)
        
    where = where.capitalize()
    context = {
        'jobs_founded': paged_jobs,
        'where_keyword': where,
        'count_rows': count_rows,
        'locations': locations,
        'org_photos':org_photos,
        'categories_for_search':categories_for_search,
        'emp_type_':emp_type_
    }
    return render(request, 'jobs/search.html', context)

def coming_soon(request):
    return render(request, 'pages/comming_soon.html')

def our_policy(request):
    return render(request, 'pages/privacy_policy.html')

def companies(request):
    org_photos = OrgModel.objects.all()

    org = Info.objects.filter(is_expired=False, status='approved').values('organzation','slug_cpn','posted_by').annotate(total=Count('slug_cpn')).order_by('-total')[:32]

    UserObj = UserProfile.objects.all()

    count_companies = Info.objects.filter(is_expired=False, status = 'approved').values('organzation').annotate(total = Count('organzation')).count()
    context = {
        'organizations': org,
        'count_companies':count_companies,
        'org_photos':org_photos,
        'UserObj':UserObj
    }
    return render(request, 'pages/companies.html',context)

def slug_companies(request, slug):
    org_photos = OrgModel.objects.all()
    
    jobs_founded = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').order_by('-activation_date','-id')
    count_rows = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').count()
    organization = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').first
    count_vac = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').annotate(as_float=Cast('no_of_jobs', IntegerField())
    ).aggregate(Sum('as_float'))
    
    
    paginator = Paginator(jobs_founded, 15)
    page = request.GET.get('page')
    try:
        paged_jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_jobs = paginator.get_page(page)

    context = {
        'jobs_founded': paged_jobs,
        'count_rows': count_rows,
        'organization': organization,
        'count_vac': count_vac,
        'org_photos':org_photos,
    }
    return render(request, 'pages/view_companies_jobs.html', context)


def slug_companies_id(request, id, slug):
    
    org_photos = OrgModel.objects.all()
    User = UserProfile.objects.get(id=id)

    jobs_founded = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').order_by('-activation_date','-id')
    count_rows = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').count()
    organization = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').values('organzation').first
    count_vac = Info.objects.filter(slug_cpn = slug, is_expired=False, status = 'approved').annotate(as_float=Cast('no_of_jobs', IntegerField())
    ).aggregate(Sum('as_float'))
    
    
    paginator = Paginator(jobs_founded, 15)
    page = request.GET.get('page')
    try:
        paged_jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_jobs = paginator.get_page(page)

    context = {
        'jobs_founded': paged_jobs,
        'count_rows': count_rows,
        'organization': organization,
        'count_vac': count_vac,
        'org_photos':org_photos,
        'UserProfile':User
    }
    return render(request, 'pages/view_companies_jobs.html', context)


def search_for_company(request):
    
    org_photos = OrgModel.objects.all()
    
    UserObj = UserProfile.objects.all()

    query_set_list = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')
    company_name = request.GET['company_name']
    #what
    if 'company_name' in request.GET:
        company_name = request.GET['company_name']
        if company_name:
            query_set_list = query_set_list.filter(organzation__icontains=company_name).values('organzation','slug_cpn','posted_by').annotate(total = Count('slug_cpn')).order_by('-total')
            count_rows = query_set_list.filter(organzation__icontains=company_name).values('organzation','slug_cpn').annotate(Count('slug_cpn')).count()
        else:
            query_set_list = query_set_list.values('organzation','slug_cpn','posted_by').annotate(total = Count('slug_cpn')).order_by('-total')
            count_rows = query_set_list.values('organzation','slug_cpn').annotate(Count('slug_cpn')).count()
    context = {
        'company_name': company_name,
        'company_found': query_set_list,
        'count_rows': count_rows,
        'org_photos':org_photos,
        'UserObj':UserObj
    }
    return render(request, 'pages/search_company.html', context)

def contact_us(request):
    
    return render(request, "pages/contact_us.html")
    

def search_for_industry(request):
    industry_query = request.GET.get('industry')


    query_set = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')
    # return HttpResponse(industry_query)

    if industry_query:
        query_set = query_set.filter(company_industry_slug__icontains=industry_query)
        count_rows = query_set.filter(company_industry_slug__icontains=industry_query).count()
    

    cities = Info.objects.filter(is_expired=False, status = 'approved').values('city','city_slug').annotate(total = Count('city')).order_by('-total')
    company_industry = Info.objects.filter(is_expired=False, status = 'approved').values('company_industry','company_industry_slug').annotate(total = Count('company_industry')).order_by('-total')
    company_type = Info.objects.filter(is_expired=False, status = 'approved').values('company_type','company_type_slug').annotate(total = Count('company_type')).order_by('-total')
    emp_type_ = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
   
    

    context = {
        'queryset':query_set,
        'cities': cities,
        'company_industry':company_industry,
        'company_type':company_type,
        'emp_type_':emp_type_,
        'count_rows':count_rows,
        'categories_for_search': categories_for_search,
        'locations': locations,
    }
    return render(request, 'filter/industry_filter.html', context)


def search_for_city(request):
    city_query = request.GET.get('city')

    query_set = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')

    if city_query:
        query_set = query_set.filter(city_slug__icontains=city_query)
        count_rows = query_set.filter(city_slug__icontains=city_query).count()

    cities = Info.objects.filter(is_expired=False, status = 'approved').values('city','city_slug').annotate(total = Count('city')).order_by('-total')
    company_industry = Info.objects.filter(is_expired=False, status = 'approved').values('company_industry','company_industry_slug').annotate(total = Count('company_industry')).order_by('-total')
    company_type = Info.objects.filter(is_expired=False, status = 'approved').values('company_type','company_type_slug').annotate(total = Count('company_type')).order_by('-total')
    emp_type_ = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
   

    context = {
        'queryset':query_set,
        'cities': cities,
        'company_industry':company_industry,
        'company_type':company_type,
        'emp_type_':emp_type_,
        'count_rows':count_rows,
        'categories_for_search': categories_for_search,
        'locations': locations,
    }

    return render(request, 'filter/city_filter.html', context)


def search_cmp_type(request):
    cmp_type_query = request.GET.get('cmp_type')
    query_set = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')

    if cmp_type_query:
        query_set = query_set.filter(company_type_slug__icontains=cmp_type_query)
        count_rows = query_set.filter(company_type_slug__icontains=cmp_type_query).count()

    cities = Info.objects.filter(is_expired=False, status = 'approved').values('city','city_slug').annotate(total = Count('city')).order_by('-total')
    company_industry = Info.objects.filter(is_expired=False, status = 'approved').values('company_industry','company_industry_slug').annotate(total = Count('company_industry')).order_by('-total')
    company_type = Info.objects.filter(is_expired=False, status = 'approved').values('company_type','company_type_slug').annotate(total = Count('company_type')).order_by('-total')
    emp_type_ = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
   
    context = {
        'queryset':query_set,
        'cities': cities,
        'company_industry':company_industry,
        'company_type':company_type,
        'emp_type_':emp_type_,
        'count_rows':count_rows,
        'categories_for_search': categories_for_search,
        'locations': locations,
    }

    return render(request, 'filter/cmp_type_filter.html', context)
    

def search_emp_type(request):
    emp_type_query = request.GET.get('emp_type')
    query_set = Info.objects.order_by('-activation_date','-id').filter(is_expired=False, status = 'approved')

    if emp_type_query:
        query_set = query_set.filter(emp_type_slug__icontains = emp_type_query)
        count_rows = query_set.filter(emp_type_slug__icontains = emp_type_query).count()

    cities = Info.objects.filter(is_expired=False, status = 'approved').values('city','city_slug').annotate(total = Count('city')).order_by('-total')
    company_industry = Info.objects.filter(is_expired=False, status = 'approved').values('company_industry','company_industry_slug').annotate(total = Count('company_industry')).order_by('-total')
    company_type = Info.objects.filter(is_expired=False, status = 'approved').values('company_type','company_type_slug').annotate(total = Count('company_type')).order_by('-total')
    emp_type_ = Info.objects.filter(is_expired=False, status = 'approved').values('emp_type','emp_type_slug').annotate(total = Count('emp_type')).order_by('-total')
    locations = Info.objects.filter(is_expired=False, status = 'approved').values('job_location').annotate(total = Count('job_location')).order_by('-total')
    categories_for_search = Info.objects.filter(is_expired=False, status = 'approved').values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')
   
    context = {
        'queryset':query_set,
        'cities': cities,
        'company_industry':company_industry,
        'company_type':company_type,
        'emp_type_':emp_type_,
        'count_rows':count_rows,
        'categories_for_search': categories_for_search,
        'locations': locations,
    }

    return render(request, 'filter/emp_type_filter.html', context)


def plain_text(request):
    file = open('/home/djangoadmin/pyapps/jobsgroup_new/templates/jobs/ads.txt', 'r')
    content = file.read()
    file.close()
    return HttpResponse(content, content_type='text/plain')
