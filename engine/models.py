from __future__ import unicode_literals

from django.db import models

# Author "has many" Books, and a Book "belongs to" a single Author
class Author(models.Model):
    name = models.CharField(max_length=100)
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)