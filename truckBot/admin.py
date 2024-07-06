from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Load, Driver, LoadHistory, LaneLoad

class UserAdmin(UserAdmin):
    fieldsets = (
      (None, {'fields': ('username', 'password')}),
      
      (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'zoom_exe_path',
                                      'zoom_phone_numb', 'landstar_firstname', 'landstar_lastname',
                                      'landstar_credentials_path', 'posting_allowed', 'banned')}),
      
      (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
      
      (('Important dates'), {'fields': ('last_login', 'date_joined')}),
  )
    
class LoadAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "pickup", "destination", "delivery", "price", "finished", "user")
    search_fields = ("id", )
  
  
class FinishedLoadsListFilter(admin.SimpleListFilter):
    title = _('load id with unfinished field')  # a label for our filter
    parameter_name = 'load_id'  # you can put here any name

    def lookups(self, request, model_admin):
        # This method should return a list of tuples. The first element in each
        # tuple is the coded value for the option that will appear in the URL query.
        # The second element is the human-readable name for the option that will
        # appear in the right sidebar.
        return [(load.id, Load.objects.get(id=load.id)) for load in Load.objects.filter(finished=False)]

    def queryset(self, request, queryset):
        # Returns the filtered queryset based on the value provided in the query string
        if self.value():
            return queryset.filter(load_id=self.value())
  
      
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "sms_sent", "load_id")
    list_filter = (FinishedLoadsListFilter, )
    search_fields = ("load_id", )

    
    def load_id(self, obj):
      return obj.load.id
  
class LoadHistoryAdmin(admin.ModelAdmin):
    list_display = ("load_id", "drivers_informed_count", "date", "user")
    search_fields = ("load_id", )
  

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(LaneLoad)
admin.site.register(Load, LoadAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(LoadHistory, LoadHistoryAdmin)
