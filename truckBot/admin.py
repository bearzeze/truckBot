from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Load, Driver, LogHistory

class UserAdmin(UserAdmin):
      fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'zoom_exe_path', 'zoom_phone_numb', 'landstar_firstname', 'landstar_lastname', 'landstar_credentials_path')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
      
      
class LoadAdmin(admin.ModelAdmin):
  list_display = ("id", "origin", "pickup", "destination", "delivery", "price")
      
class DriverAdmin(admin.ModelAdmin):
  list_display = ("name", "phone_number", "sms_sent", "load_id")
  
  def load_id(self, obj):
    return obj.load.id

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Load, LoadAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(LogHistory)
