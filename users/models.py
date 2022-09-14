from importlib.metadata import requires
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)

    def __repr__(self):
        return self.title
