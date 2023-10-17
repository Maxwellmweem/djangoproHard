from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.admin import AdminSite
from django.urls import path,reverse
from django.utils.html import mark_safe
from .models import Account 
from .models import Member
from .models import BiometricData
from django.utils.html import format_html
from django.utils.safestring import mark_safe





class CustomAdminSite(AdminSite):
    login_template = 'login.html'

    def login(self, request, extra_context=None):
        return LoginView.as_view(template_name=self.login_template)(request)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('login/', self.login, name='login'),
        ]
        return custom_urls + urls
        

admin.site = CustomAdminSite(name='admin')
    
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()  

admin.site.register(Account, AccountAdmin) 


class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone_number','registration_date')
    list_filter = ('account',) 


    filter_horizontal = () 
    fieldsets = ()     

admin.site.register(Member,MemberAdmin) 

class BiometricDataAdmin(admin.ModelAdmin):
    list_display = ('account_email', 'recorded_audio_link', 'captured_face_link')  # Updated field name here
    list_filter = ('account',)
    search_fields = ('account__email',)

    def account_email(self, obj):
        return obj.account.email

    account_email.short_description = 'Account Email'

    def recorded_audio_link(self, obj):
        if obj.recorded_audio:  # Updated field name here
            return '<a href="{0}" target="_blank">{1}</a>'.format(obj.recorded_audio.url, "Recorded Audio")  # Updated field name here
        return 'No audio'

    recorded_audio_link.short_description = 'Recorded Audio'  # Updated field name here
    recorded_audio_link.allow_tags = True

    def captured_face_link(self, obj):
        if obj.captured_face:
            return '<a href="{0}" target="_blank">{1}</a>'.format(obj.captured_face.url, "Captured Face")
        return 'No image'

    captured_face_link.short_description = 'Captured Face'
    captured_face_link.allow_tags = True

admin.site.register(BiometricData, BiometricDataAdmin)






