from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 用户信息
class User(AbstractUser):
    # 电话号码字段
    # unique 为唯一性字段
    mobile = models.CharField(max_length=20, unique=True, blank=False)

    # 头像
    # upload_to为保存到相应的子目录中
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    # 个人简介
    user_desc = models.TextField(max_length=500, blank=True)

    # 修改认证的字段
    USERNAME_FIELD = 'mobile'

    # 创建超级管理员时需要必须设置的字段(不包括手机号和密码)
    REQUIRED_FIELDS = ['username', 'email']

    # 内部类class Meta 用于给model定义元数据
    class Meta:
        db_table = "tb_users"  # 修改默认表名字
        verbose_name = "用户管理"  # admin后台显示
        verbose_name_plural = verbose_name  # admin后台显示

    def __str__(self):
        return self.mobile
