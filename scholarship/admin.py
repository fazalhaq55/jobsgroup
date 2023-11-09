from django.contrib import admin
from .models import Detail
class InfoAdmin(admin.ModelAdmin):

        
    list_display = ('scholarship_title',)
    
    # list_display_links = ('id','job_title')
    # list_filter = ('job_date','is_expired')
    # list_editable = ('is_expired',)
    # search_fields = ('job_title','job_location','vacancy_number','organzation')
    # list_per_page = 500
    # exclude = ('favourite','url')
    
admin.site.register(Detail, InfoAdmin)
