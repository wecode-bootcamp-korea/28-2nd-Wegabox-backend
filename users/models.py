from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    email    = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'users'