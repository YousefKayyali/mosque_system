from django.db import models
from user_auth.models import Profiles,Users,Students
class QuranMemorization(models.Model):
    memorization_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey('user_auth.Students', models.DO_NOTHING)
    record_date = models.DateTimeField()
    memorization_type = models.CharField(max_length=10)
    user = models.ForeignKey('user_auth.Users', models.DO_NOTHING)
    from_page = models.SmallIntegerField()
    to_page = models.SmallIntegerField()
    evaluation = models.CharField()
    number_of_misses = models.SmallIntegerField()
    note = models.TextField(blank=True, null=True)
    from_verse = models.SmallIntegerField()
    to_verse = models.SmallIntegerField()
    class Meta:
        managed = False
        db_table = 'quran_memorization'
class Points(models.Model):
    pk = models.CompositePrimaryKey('point_id', 'student_id')
    point_id = models.BigIntegerField()
    student = models.ForeignKey('user_auth.Students', models.DO_NOTHING)
    point = models.SmallIntegerField()
    note = models.TextField(blank=True, null=True)
    date_of_insert = models.DateField()

    class Meta:
        managed = False
        db_table = 'points'