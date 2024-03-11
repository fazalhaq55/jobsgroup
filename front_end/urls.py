from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about', views.about, name = 'about'),
    path('search', views.search, name = 'search'),
    path('jobs-by-location/<str:where>', views.searchJob, name='jobs-by-location'),
    path('our-policy',views.our_policy, name="our-policy"),
    path('companies', views.companies, name="companies"),
    path('companies/<str:slug>', views.slug_companies, name="companies"),
    path('companies/<int:id>/<str:slug>', views.slug_companies_id, name="companies"),
    path('search-company', views.search_for_company, name="search-company"),
    path('contact-us', views.contact_us, name="contact-us"),
    path('search_industry', views.search_for_industry, name='search_industry'),
    path('search_city', views.search_for_city, name='search_city'),
    path('search_cmp_type', views.search_cmp_type, name="search_cmp_type"),
    path('search_emp_type', views.search_emp_type, name='search_emp_type'),
    path('ads.txt', views.plain_text, name='ads.txt')
]