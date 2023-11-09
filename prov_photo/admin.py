from django.contrib import admin
from django.urls import path
from prov_photo.models import info
from django.shortcuts import render

class InfoAdmin(admin.ModelAdmin):
        
    list_display = ('id', 'name')
    list_display_links = ('id','name')
    search_fields = ('name',)

admin.site.register(info, InfoAdmin)
