from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField("Event", related_name='particepant')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name
