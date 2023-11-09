from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', views.index, name = 'index'),
    path('login', views.login_view, name = 'login'),
    path('register', views.register, name = 'register'),
    path('home', views.home, name='home'),
    path('logout', views.logout_user, name='logout'),
    path('add_job', views.add_job, name='add_job'),
    # path('save_job/', views.save_job, name='save_job'),
    path('settings/', views.settings, name='settings'),
    path('job_listing/<int:id>/', views.job_listing, name='job_listing'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('edit/<int:id>/', views.edit_job, name="edit"),

    path('reset_password/', views.password_reset_request, name="reset_password"),   

    path('reset_password_sent/', 
          auth_views.PasswordResetDoneView.as_view(template_name="Employer/reset_password_sent.html"), 
          name="password_reset_done"),   
          
    path('reset/<uidb64>/<token>', 
          auth_views.PasswordResetConfirmView.as_view(template_name = 'Employer/password_reset_form.html'),
          name="password_reset_confirm"),   

    path('reset_password_complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name="Employer/reset_password_done.html"),
          name="password_reset_complete"),   

    # 1 - Submit email form  -----------------------PasswordResetView.as_view()
    # 2 - Email sent success message ---------------PasswordResetDoneView.as_view()
    # 3 - Link to password reset form in email -----PasswordResetConfirmView.as_view()
    # 4 - Password successfully changed message ----PasswordResetCompleteView.as_view()
    
    
       
]