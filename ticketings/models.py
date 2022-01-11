from django.db     import models

from core.models   import TimeStampModel
from movies.models import Movie
from users.models  import User

class Schedule(models.Model):
    movie        = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater      = models.ForeignKey('Theater', on_delete=models.CASCADE)
    running_date = models.DateField() 
    start_time   = models.TimeField()
    end_time     = models.TimeField()

    class Meta:
        db_table = 'schedules'

class Region(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'regions'

class Theater(models.Model):
    name   = models.CharField(max_length=50)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)

    class Meta:
        db_table = 'theaters'

class Ticketing(TimeStampModel):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ticketings'