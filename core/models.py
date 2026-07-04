from django.db import models
from user_auth.models import Profiles,Users,Students
class QuranMemorization(models.Model):
    memorization_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('user_auth.Students', models.DO_NOTHING)
    record_date = models.DateTimeField()
    memorization_type = models.CharField(max_length=12)
    user = models.ForeignKey('user_auth.Users', models.DO_NOTHING)
    from_page = models.SmallIntegerField()
    evaluation = models.CharField()
    number_of_misses = models.SmallIntegerField()
    note = models.TextField(blank=True, null=True)
    pages = models.FloatField()
    class Meta:
        managed = False
        db_table = 'quran_memorization'

class Points(models.Model):
    point_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('user_auth.Students', models.DO_NOTHING)
    note = models.TextField(blank=True, null=True)
    date_of_insert = models.DateField()
    point = models.SmallIntegerField(blank=True, null=False)
    class Meta:
        managed = False
        db_table = 'points'
        unique_together = ('student', 'date_of_insert') 