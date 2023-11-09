from django.urls import path
from . import views

urlpatterns = [
    path('', views.scholarship, name='scholarships'),
    path('<int:id>/<str:slug>', views.scholarship_details, name="scholarships"),
    path('search-for-scholarship', views.search_scholarship, name = 'search-for-scholarship'),
    path('scholarships/countries/<str:where>', views.by_country, name='scholarships.countries'),
    path('scholarships/organization/<str:where>', views.by_organization, name='scholarships.organization'),
    path('degree/<str:degree>', views.by_degree_scholarships, name="degree"),
    path('field-of-studies', views.field_of_study, name="field-of-studies"),
    path('<str:field>', views.view_by_field, name="")
    # path('filter-data', views.filter_data, name="scholarships.filter_data")
]