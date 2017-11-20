from django.db import models

# Create your models here.


class User(models.Model):
    """
    User Table
    """
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    email = models.CharField(max_length=128, verbose_name="邮箱")

    role = models.ManyToManyField(to="Role", verbose_name="用户所具有的角色", blank=True)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    Role Table

    通过角色表整合权限，减少用户与权限的直接关联
    """
    title = models.CharField(max_length=32, verbose_name="角色名")

    permission = models.ManyToManyField(to="Permission", verbose_name="角色所持有的权限", blank=True)

    class Meta:
        verbose_name_plural = "Role"

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    Permission Table

    权限表是权限管理的最小单元；
    通过组内菜单划分权限内权限的主次；
    通过组对权限进行归纳划分；
    """
    title = models.CharField(max_length=32, verbose_name="别名")
    url = models.CharField(max_length=64, verbose_name="URL")
    code = models.CharField(max_length=32, verbose_name="code")

    group_menu = models.ForeignKey(to="Permission", verbose_name="所属组内菜单", blank=True, null=True, related_name="xx")
    group = models.ForeignKey(to="PermissionGroup", verbose_name="所属组")

    class Meta:
        verbose_name_plural = "Permission"

    def __str__(self):
        return self.title


class PermissionGroup(models.Model):
    """
    Permission Group Table

    权限组是对权限的整合
    """
    title = models.CharField(max_length=32, verbose_name="权限组名称")
    menu = models.ForeignKey(to="Menu", verbose_name="所属菜单")

    class Meta:
        verbose_name_plural = "Permission Group"

    def __str__(self):
        return self.title


class Menu(models.Model):
    """
    Menu Table

    菜单是对权限组的进一步整合
    """
    title = models.CharField(max_length=32, verbose_name="菜单名")

    class Meta:
        verbose_name_plural = "Menu"

    def __str__(self):
        return self.title
