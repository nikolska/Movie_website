from django.db import models
from django.urls import reverse


class Person(models.Model):
    """Movie's person model"""

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='people/')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """Get url to the single person"""
        return reverse('person_details', args=[str(self.pk)])

    class Meta:
        ordering = ['first_name']


class Genre(models.Model):
    """Movie's genre model"""

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Movie(models.Model):
    """Movie's model with all necessary information"""

    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='director')
    screenplay = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='screenplay')
    starring = models.ManyToManyField(Person, through='PersonMovie')
    year = models.IntegerField(max_length=4)
    rating = models.FloatField(default=1.0)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='movies/', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Get url to the single movie"""
        return reverse('movie_details', args=[str(self.pk)])

    class Meta:
        ordering = ['title']


class PersonMovie(models.Model):
    """Movie's cast model (only starring)"""

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, default='cast')

    def __str__(self):
        return f'{self.person} / {self.movie}'

    class Meta:
        ordering = ['movie']
