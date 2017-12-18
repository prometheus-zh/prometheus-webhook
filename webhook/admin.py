# coding: utf-8
from django.contrib import admin
from webhook.models import *
from django.contrib import admin
from webhook.models import CmsUser, CmsGroup
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

admin.AdminSite.site_header = "告警配置"
admin.AdminSite.site_title = "告警配置"

class Email_ConfigAdmin(admin.ModelAdmin):
    list_display = ['smtp_host','smtp_port']


class Sms_ConfigAdmin(admin.ModelAdmin):
    list_display = ['api_key']


class Allow_IpAdmin(admin.ModelAdmin):
    list_display = ['ip']


class SmtpConfig(forms.ModelForm):
    ssl_radio = ((0, 'No'), (1, 'Yes'))
    smtp_ssl = forms.TypedChoiceField(
                     choices=ssl_radio, widget=forms.RadioSelect, coerce=int
                )


class WechatConfig(admin.ModelAdmin):
    list_display =['wechat_id']


class SmsLog(admin.ModelAdmin):
    list_display = ['phone','content','date']

    def has_add_permission(self, request):
        return False

   # def has_delete_permission(self, request, obj=None):
   #     return False

    def save_model(self, request, obj, form, change):
        return False

   # def delete_model(self, request, obj):
   #     return False
    def save_related(self, request, form, formsets, change):
        return False

class EmailLog(admin.ModelAdmin):
    list_display = ['email','content', 'status', 'date']
    def has_add_permission(self, request):
        return False

    #def has_delete_permission(self, request, obj=None):
    #    return False

    def save_model(self, request, obj, form, change):
        return False

    #def delete_model(self, request, obj):
    #    return False

    def save_related(self, request, form, formsets, change):
        return False


class WechatLog(admin.ModelAdmin):
    list_display = ['wechat', 'content', 'status', 'date']
    def has_add_permission(self, request):
        return False

    #def has_delete_permission(self, request, obj=None):
    #    return False

    def save_model(self, request, obj, form, change):
        return False

    #def delete_model(self, request, obj):
    #    return False

    def save_related(self, request, form, formsets, change):
        return False

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='密码', widget=forms.HiddenInput(),initial="123456" )
    password2 = forms.CharField(label='重复密码', widget=forms.HiddenInput(),initial="123456")
    class Meta:
        model = CmsUser
        fields = ('username',)
    def clean_password2(self):
        password1 = '123456'
        password2 = '123456'
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):


    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CmsUser
        fields = ('email', 'password', 'is_active', 'is_admin')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'remarks')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'phone', 'wechat_id', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
      #  ('Primary info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('username', 'email', 'wechat_id', 'phone', 'group')}),

    )
    add_fieldsets = (
        ('Add user', {
            'classes': ('wide',),
            'fields': ('username', 'email',  'phone', 'wechat_id', 'password1', 'password2', 'group')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('group',)


admin.site.register(Email_Config, Email_ConfigAdmin)
admin.site.register(Wechat_Config, WechatConfig)
admin.site.register(Sms_Config, Sms_ConfigAdmin)
admin.site.register(Allow_Ip, Allow_IpAdmin)
admin.site.register(CmsUser, UserAdmin)
admin.site.register(CmsGroup, GroupAdmin)
admin.site.register(Email_Log, EmailLog)
admin.site.register(Wechat_Log, WechatLog)
admin.site.register(Sms_Log, SmsLog)
admin.site.unregister(Group)
