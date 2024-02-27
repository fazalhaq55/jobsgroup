from django.contrib import admin
from django.urls import path
from .models import Info
from django.shortcuts import render

class InfoAdmin(admin.ModelAdmin):

    # def is_published_n(self, obj):
    #     if obj.job_location == "Kabul":
    #         id = obj.id
    #         record = Info.objects.filter(pk=id).update(is_published=True)
    #         return obj.is_published
    #     elif obj.job_location != "Kabul":
    #         n_id = obj.id
    #         record = Info.objects.filter(pk=n_id).update(is_published=False)
            # return obj.is_published
        
    list_display = ('id', 'job_title','slug_cpn','is_expired')
    
    list_display_links = ('id','job_title')
    list_filter = ('job_date','is_expired','work_from_home')
    list_editable = ('is_expired',)
    search_fields = ('job_title','job_location','organzation')
    list_per_page = 500
    exclude = ('url',)

    # TO MAKE CUSTOM URL AND CUSTOM VIEW FUNCTION
    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('my_view/', self.admin_site.admin_view(self.my_view))
    #     ]
    #     return my_urls + urls
    # def my_view(self, request):
    #     # if self.model.Info.objects.filter(headline="Test"):
    #     return render(request, "admin/NoneJobs.html")
# admin.site.site_header = 'Jobs Tracker'
admin.site.register(Info, InfoAdmin)
# admin.site.register(ModelName, ModelClassName)
