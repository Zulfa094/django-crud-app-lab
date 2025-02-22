from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

LISTENING_TIMES = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)

class Track(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("track-detail", kwargs={"pk": self.pk})

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracks = models.ManyToManyField('Track')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("album-detail", kwargs={"album_id": self.id})

class Listen(models.Model):
    date = models.DateField()
    time = models.CharField(
        max_length=1,
        choices=LISTENING_TIMES,
        default=LISTENING_TIMES[0][0]
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_time_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']
