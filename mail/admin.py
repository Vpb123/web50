from django.contrib import admin

# Register your models here.
from .models import User, Email;
class EmailAdmin(admin.ModelAdmin):
    list_display=['user','sender','subject','body','timestamp']
admin.site.register(User)
admin.site.register(Email,EmailAdmin)