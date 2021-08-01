from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active') #quiero que se muestren en la administracion
    list_display_links = ('email','first_name','last_name') #campos que quiero sean clickeables
    readonly_fields = ('last_login','date_joined') #campos que no quiero modificar
    ordering = ('-date_joined',) # ordena por fecha de ingreso
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="50" style="border-radius:50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'Profile picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    
    
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)