from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager
from django.db import models
from django.contrib.auth.hashers import make_password

class Profiles(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    created_date = models.DateField(blank=True,null=True)
    is_active = models.BooleanField(blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'profiles'
class Privileges(models.Model):
    privilege_id = models.BigAutoField(primary_key=True)
    privilege_name = models.CharField(unique=True, max_length=50)
    privilege_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'privileges'
class ProfilesPrivilege(models.Model):
    pk = models.CompositePrimaryKey('profile_id', 'privilege_id')
    profile = models.ForeignKey(Profiles, models.DO_NOTHING)
    privilege = models.ForeignKey(Privileges, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profiles_privilege'
class Students(models.Model):
    student_id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profiles, models.DO_NOTHING)
    guardian_phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'students'
class Users(AbstractBaseUser,PermissionsMixin):
    user_id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profiles, models.DO_NOTHING)
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(unique=True, max_length=20)
    USERNAME_FIELD='username'
    last_login = None
    is_superuser = None
    objects=UserManager()
    class Meta:
        managed = False
        db_table = 'users'
    def save(self,*args,**kwargs):
        self.password=make_password(self.password)
        super().save(*args,**kwargs)
class Absences(models.Model):
    pk = models.CompositePrimaryKey('student_id', 'day_date')
    student = models.ForeignKey('Students', models.DO_NOTHING)
    day_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'absences'


