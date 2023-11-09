from django.contrib import admin
from .models import Message

class UserAdminPanel(admin.ModelAdmin):
    list_display = ('user_name','user_email','user_message')
    search_fields = ('user_name','user_email','user_message')
    list_filter = ('user_name','user_email')
    
admin.site.register(Message, UserAdminPanel)