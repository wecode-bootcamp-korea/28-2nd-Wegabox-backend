from django.db         import models

class Movie(models.Model):
    title         = models.CharField(max_length=50)
    description   = models.CharField(max_length=100)
    thumbnail_url = models.URLField(max_length=2000)
    release_date  = models.DateField()

    class Meta:
        db_table = 'movies'