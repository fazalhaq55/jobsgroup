from django.contrib import admin
from .models import Form

class applicationAdminPanel(admin.ModelAdmin):
    list_display = ('title','description','company','filename')
    search_fields = ('title','company')
    list_filter = ('title','company')
    
admin.site.register(Form, applicationAdminPanel)