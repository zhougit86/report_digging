from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Report(models.Model):
    code=models.TextField()
    urls=models.URLField(unique=True,default='000')
    title=models.TextField()

    def __repr__(self):
        return self.code+self.title


class Report_detail(models.Model):
    code=models.TextField()
    urls=models.URLField(unique=True,default='000')
    facility=models.TextField()
    title = models.TextField()
    date = models.TextField()

    def __repr__(self):
        return self.code+self.title
    # def __str__(self):
    #     return self.code+self.title+self.date
