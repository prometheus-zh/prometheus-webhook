# coding: utf-8

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
#import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')






class CmsUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        '''username 是唯一标识，没有会报错'''
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)  # 检测密码合理性
        user.save(using=self._db)  # 保存密码
        return user
    def create_superuser(self, username, email, password):
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                )
        user.is_admin = True  # 比创建用户多的一个字段
        user.save(using=self._db)
        return user



class CmsUser(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, db_index=True,verbose_name='姓名')
    email = models.EmailField(max_length=255, unique=True, blank=True)
    phone = models.CharField(max_length=11,verbose_name="电话号码",blank=True,null=True)
    name = models.CharField(max_length=100, verbose_name='中文名',blank=True,null=True)
    head_img = models.ImageField(blank=True, upload_to="uploads/portrait", verbose_name='头像')
    group = models.ManyToManyField('CmsGroup',verbose_name='所属告警组')
    create_date = models.DateField(auto_now=True, verbose_name='创建时间')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'  # 必须有一个唯一标识--USERNAME_FIELD
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # 创建superuser时的必须字段

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.username
    '''django自带后台权限控制，对哪些表有查看权限等'''
    def has_perm(self, perm, obj=None):
        return True
    '''用户是否有权限看到app'''
    def has_module_perms(self, app_label):
        return True
    def __str__(self):  # __unicode__ on Python 2
        return self.username
    @property
    def is_staff(self):
        return self.is_admin
    class Meta:
        verbose_name = '告警用户'
        verbose_name_plural = '告警用户'
        permissions = (
            ("view_users", "Can see available userlist"),
        )
    objects = CmsUserManager()  # 创建用户

class CmsGroup(models.Model):
    name = models.CharField(max_length=64, verbose_name='部门')
    remarks = models.CharField(max_length=64, blank=True, verbose_name='备注')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '告警用户组'
        verbose_name_plural = '告警用户组'

class Sms_Config(models.Model):
    api_key = models.CharField(verbose_name="云片网短信密钥配置",max_length=70,unique=True)

    class Meta:
        verbose_name_plural = u'云片网短信密钥'


class Email_Config(models.Model):
    smtp_host = models.CharField(verbose_name="邮件主机配置",max_length=70,unique=True)
    smtp_port = models.IntegerField(verbose_name="邮件端口配置")
    smtp_user = models.CharField(verbose_name="邮件登录用户",max_length=70)
    smtp_pass = models.CharField(verbose_name="邮件登录密码",max_length=70)
    smtp_ssl = models.BooleanField(verbose_name="SSL",default=False)

    class Meta:
        verbose_name_plural = u'邮件账户配置'




class Sms_Log(models.Model):
    phone = models.CharField(max_length=500,blank=True,null=True)
    content = models.CharField(max_length=500,blank=True,null=True)
    status = models.CharField(max_length=500,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        verbose_name_plural = u'短信日志'

class Email_Log(models.Model):
    email = models.CharField(max_length=500,blank=True,null=True)
    content = models.CharField(max_length=500,blank=True,null=True)
    status = models.CharField(max_length=500,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        verbose_name_plural = u'邮件日志'


class Allow_Ip(models.Model):
    ip = models.GenericIPAddressField(unique=True)

    class Meta:
        verbose_name_plural = u'Ip白名单'
