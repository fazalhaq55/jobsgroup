from django.urls import path
from . import views

urlpatterns = [
    path('', views.jobs, name = 'jobs'),
    path('<int:id>/<str:slug>', views.job_details, name = ''),
    path('categories/<slug:slug>', views.category, name="category"), 
    path('application_form', views.application_form, name='application_form'),
    path('apply/<int:id>/<str:slug>', views.apply, name="apply"),
    path('ads.txt', views.plain_text, name='ads')
]