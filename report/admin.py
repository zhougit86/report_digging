from django.contrib import admin

# Register your models here.
from django.contrib import admin
from report.models import Report,Report_detail

admin.site.register(Report)
admin.site.register(Report_detail)
