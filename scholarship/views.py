from django.shortcuts import render
from scholarship.models import Detail
from jobs.models import Info
from django.db.models import Count
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Sum
import datetime
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from org_photo.models import info as OrgModel

# Create your views here.
def scholarship(request):
    
    myDate = datetime.date.today()
    today = myDate.strftime("%Y-%m-%d")
    record = Detail.objects.filter(is_expired=False)
    for i in record:
        if(i.deadline):
            if (i.deadline < today):
                i.is_expired = True
                i.save()

    scholarships = Detail.objects.all().order_by('-id')            
    locations = Detail.objects.values('country').annotate(total = Count('country')).order_by('-total')
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]
    area_of_study = Detail.objects.values('field_of_stady').annotate(total=Count('field_of_stady'))
    opp_type = Detail.objects.values('opp_type').annotate(total=Count('opp_type'))
    paginator = Paginator(scholarships, 15)
    page = request.GET.get('page')
    try:
        paged_scholarships = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_scholarships = paginator.get_page(page)

    context = {
        'scholarships':paged_scholarships,
        'footer_categories': footer_categories,
        'country':locations,
        'area_of_study':area_of_study,
        'opp_type':opp_type
    }
    return render(request, 'scholarship/index.html', context)

def scholarship_details(request, id, slug):
    
    myDate = datetime.date.today()
    today = myDate.strftime("%Y-%m-%d")
    record = Detail.objects.filter(is_expired=False)
    for i in record:
        if(i.deadline):
            if (i.deadline < today):
                i.is_expired = True
                i.save()
            
    scho_details = Detail.objects.filter(opp_slug=slug, id = id).first()
    org_photos = OrgModel.objects.all()

    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]

    if scho_details:
        
        scho_details.views = scho_details.views + int(1)
        scho_details.save()
        
    context = {
        'scho_details': scho_details,
        'footer_categories': footer_categories,
        'org_photos': org_photos
    }
    return render(request, 'scholarship/scho_details.html', context)


def search_scholarship(request):
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]
    locations = Detail.objects.filter(is_expired=False).values('country').annotate(total = Count('country')).order_by('-total')
   
    query_set_list = Detail.objects.order_by('-id').filter(is_expired=False)
    count_rowss = Detail.objects.all().filter(is_expired=False).count()
    what = request.GET['what']
    where = request.GET['where']
    #what
    if 'what' in request.GET:
        what = request.GET['what']
        if what:
            query_set_list = query_set_list.filter(scholarship_title__icontains=what)
            count_rows = query_set_list.filter(scholarship_title__icontains=what).count()
        else:
            query_set_list = query_set_list
            count_rows = count_rowss
    if 'where' in request.GET:
        where = request.GET['where']
        if where:
            query_set_list = query_set_list.filter(country__iexact=where)
            count_rows = query_set_list.filter(country__iexact=where).count()
        else:
            query_set_list = query_set_list

    context = {
        'scho_founded': query_set_list,
        'what_keyword': what,
        'where_keyword': where,
        'count_rows': count_rows,
        'footer_categories' : footer_categories,
        'country' : locations,
    }
    return render(request, 'scholarship/search.html', context)

def by_country(request, where):
    
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]

    country = Detail.objects.filter(country_slug = where).first
    # This following query will return the all opportunites related to the where organization
    count_vac = Detail.objects.filter(country_slug = where).annotate(as_float=Cast('number_of_opp', IntegerField())
    ).aggregate(Sum('as_float'))
    query_set_list = Detail.objects.order_by('-id')

    if where:
        query_set_list = query_set_list.filter(country_slug__iexact=where)
        count_rows = query_set_list.filter(country_slug__iexact=where).count()
        
    paginator = Paginator(query_set_list, 15)
    page = request.GET.get('page')
    try:
        paged_scho = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_scho = paginator.get_page(page)
        
    where = where.capitalize()
    context = {
        'scho_founded': paged_scho,
        'where_keyword': where,
        'count_rows': count_rows,
        'footer_categories' : footer_categories,
        'country':country,
        'count_vac': count_vac
    }
    return render(request, 'scholarship/by_country.html', context)



def by_organization(request, where):
    
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]

    organization = Detail.objects.filter(organization_slug = where).first
    # This following query will return the all opportunites related to the where organization
    count_vac = Detail.objects.filter(organization_slug = where).annotate(as_float=Cast('number_of_opp', IntegerField())
    ).aggregate(Sum('as_float'))
    query_set_list = Detail.objects.order_by('-id')

    if where:
        query_set_list = query_set_list.filter(organization_slug__iexact=where)
        count_rows = query_set_list.filter(organization_slug__iexact=where).count()
        
    paginator = Paginator(query_set_list, 15)
    page = request.GET.get('page')
    try:
        paged_scho = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_scho = paginator.get_page(page)
        
    where = where.capitalize()
    context = {
        'scho_founded': paged_scho,
        'where_keyword': where,
        'count_rows': count_rows,
        'footer_categories' : footer_categories,
        'organization':organization,
        'count_vac': count_vac
    }
    return render(request, 'scholarship/by_organization.html', context)

def by_degree_scholarships(request, degree):
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]
    count_vac = Detail.objects.filter(level__icontains = degree).annotate(as_float=Cast('number_of_opp', IntegerField())
    ).aggregate(Sum('as_float'))

    query_set_list = Detail.objects.order_by('-id')

    if degree:
        query_set_list = query_set_list.filter(level__icontains=degree)
        count_rows = query_set_list.filter(level__icontains=degree).count()
        
    paginator = Paginator(query_set_list, 15)
    page = request.GET.get('page')
    try:
        paged_scho = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_scho = paginator.get_page(page)
        
    degree = degree.capitalize()

    
    context = {
        'scho_founded': paged_scho,
        'degree': degree,
        'count_rows': count_rows,
        'footer_categories' : footer_categories,
        'count_vac': count_vac
    }
    return render(request, 'scholarship/by_degree.html', context)


def field_of_study(request):
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]
    fields = Detail.objects.all().values('field_of_stady').annotate(total = Count('field_of_stady'))
    context = {
        'footer_categories' : footer_categories,
        'fields': fields
    }
    return render(request, 'scholarship/field_of_study.html', context)



def view_by_field(request, field):
    footer_categories = Info.objects.filter(is_expired=False).values('category', 'slug_cate').annotate(total = Count('category')).order_by('-total')[:7]
    count_vac = Detail.objects.filter(field_of_stady__icontains = field).annotate(as_float=Cast('number_of_opp', IntegerField())
    ).aggregate(Sum('as_float'))

    query_set_list = Detail.objects.order_by('-id')

    if field:
        query_set_list = query_set_list.filter(field_of_stady__icontains=field)
        count_rows = query_set_list.filter(field_of_stady__icontains=field).count()
        
    paginator = Paginator(query_set_list, 15)
    page = request.GET.get('page')
    try:
        paged_scho = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        paged_scho = paginator.get_page(page)
        
    field = field.capitalize()

    
    context = {
        'scho_founded': paged_scho,
        'field': field,
        'count_rows': count_rows,
        'footer_categories' : footer_categories,
        'count_vac': count_vac
    }
    return render(request, 'scholarship/by_field.html', context)

# Filter data function

# def filter_data(request):
#     type = request.GET.getlist('opp_type[]')
#     field_of_study = request.GET.getlist('field_of_study[]')
#     all_scholarships = Detail.objects.all().order_by('-id')

#     filtered= Detail.objects.filter(opp_type__icontains=type).distinct()
    
#     # return HttpResponse(type)
#     t=render_to_string('scholarship/ajax_filter.html', {'data':filtered})
#     return JsonResponse({'data':t})

# the solution is to add template scholarship,fellowship manually and give them id