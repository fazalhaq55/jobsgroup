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
]