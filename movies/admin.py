from django.contrib import admin
from .models import Genre, Movie, Person, PersonMovie


admin.site.register(Person)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(PersonMovie)
