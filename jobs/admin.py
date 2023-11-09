from django.contrib import admin
from django.urls import path
from .models import Info
from django.shortcuts import render

class InfoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
       obj.approve_post()
    # def is_published_n(self, obj):
    #     if obj.job_location == "Kabul":
    #         id = obj.id
    #         record = Info.objects.filter(pk=id).update(is_published=True)
    #         return obj.is_published
    #     elif obj.job_location != "Kabul":
    #         n_id = obj.id
    #         record = Info.objects.filter(pk=n_id).update(is_published=False)
            # return obj.is_published
    
    list_display = ('id','meta_tag', 'job_title','salary','education','organzation','is_expired','status', 'activation_date')
    
    list_display_links = ('id','job_title','meta_tag')
    list_filter = ('job_date','is_expired')
    list_editable = ('is_expired','status',)
    search_fields = ('job_title','job_location','vacancy_number','organzation')
    list_per_page = 50
    exclude = ('favourite','url')

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
