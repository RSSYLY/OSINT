from django.db import models

# Create your models here.

# 自定义用户模型
# 内置的用户模型是django.contrib.auth.models.User，包含了用户名、密码、邮箱等字段，但是如果你想要添加其他字段，就需要自定义用户模型了。

from django.contrib.auth.models import AbstractUser
from django.db import models

# 添加邮箱、手机号字段


class CustomUser(AbstractUser):
    username = models.CharField(verbose_name="用户名", max_length=10, unique=True)
    password = models.CharField(verbose_name="密码", max_length=30)
    email = models.EmailField(verbose_name="邮箱", max_length=30, unique=True)
    # 手机号码可以为空，但不能重复，但是考虑到空也可以重复
    phone = models.CharField(verbose_name="手机号码", max_length=15, null=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = "user"
        unique_together = ['phone', 'email']
