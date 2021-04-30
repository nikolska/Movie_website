from datetime import date
from itertools import chain

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from .forms import (
    MovieForm, PersonForm,
    SearchMovieForm, SearchPersonForm
)
from .models import Genre, Movie, Person, PersonMovie


class MoviesListView(FormView, ListView):
    """Home page with list of movies and form to search movie by the title, year, rating, genre and cast"""

    model = Movie
    context_object_name = 'movies'
    template_name = 'movies_list.html'
    form_class = SearchMovieForm
    success_url = reverse_lazy('movies_list')

    def get_queryset(self):
        """Return the list of items for this view"""

        title = self.request.GET.get('title')
        genre = self.request.GET.getlist('genre')
        cast_name = self.request.GET.get('cast_name')
        year_from = self.request.GET.get('year_from')
        year_to = self.request.GET.get('year_to')
        rating_from = self.request.GET.get('rating_from')
        rating_to = self.request.GET.get('rating_to')

        object_list = Movie.objects.all()
        data = title, genre, cast_name, year_from, year_to, rating_from, rating_to

        if any(data):
            title = title if title else ''
            genre = genre if genre else Genre.objects.all()
            year_from = int(year_from) if year_from else 0
            year_to = int(year_to) if year_to else int(date.today().year)
            rating_from = float(rating_from) if rating_from else 0
            rating_to = float(rating_to) if rating_to else 10
            cast_name = cast_name if cast_name else ''
            cast_name_list = Person.objects.filter(
                Q(first_name__icontains=cast_name) |
                Q(last_name__icontains=cast_name)
            ).distinct()

            movie_list = []
            for name in cast_name_list:
                movies = Movie.objects.filter(
                    Q(director=name) |
                    Q(screenplay=name) |
                    Q(starring=name),
                    title__icontains=title,
                    year__range=(year_from, year_to),
                    rating__range=(rating_from, rating_to),
                    genre__in=genre,
                ).distinct()
                movie_list.append(movies)

            object_list = list(set(chain(*movie_list)))
            return object_list
        else:
            return object_list


class MovieCreateView(CreateView):
    """Movie create page"""

    model = Movie
    template_name = 'add_movie.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_details')

    def get_success_url(self, **kwargs):
        return reverse("movie_details", kwargs={'pk': self.object.pk})


class MovieDetailView(DetailView):
    """Page with movie's details like poster, genres, director, screenplay, starring etc."""

    model = Movie
    template_name = 'movie_details.html'

    def get_context_data(self, **kwargs):
        """Insert the object into the context dict"""

        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        starring = PersonMovie.objects.filter(movie=movie, role__contains='cast').order_by('person')
        stars = Person.objects.all()
        ctx = super().get_context_data(**kwargs)
        ctx['starring'] = starring
        ctx['stars'] = stars
        return ctx


class MovieUpdateView(UpdateView):
    """Edit movie's details"""

    model = Movie
    form_class = MovieForm
    template_name = 'movie_edit.html'


class MovieDeleteView(DeleteView):
    """Movie delete view"""

    model = Movie
    template_name = 'del_movie.html'
    success_url = reverse_lazy('movies_list')

    def get_context_data(self, **kwargs):
        """Insert the object into the context dict"""

        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        ctx = super().get_context_data(**kwargs)
        ctx['movie'] = movie
        return ctx


class StarsListView(FormView, ListView):
    """Movies stars list with search form"""

    model = Person
    context_object_name = 'stars'
    template_name = 'stars_list.html'
    form_class = SearchPersonForm
    success_url = reverse_lazy('stars_list')

    def get_queryset(self):
        """Return the list of items for this view"""

        search = self.request.GET.get('search')
        if search:
            return Person.objects.filter(
                            Q(first_name__icontains=search) |
                            Q(last_name__icontains=search)).distinct()
        else:
            return Person.objects.all()


class PersonCreateView(CreateView):
    """Person create page"""

    model = Person
    form_class = PersonForm
    template_name = 'create_person.html'
    success_url = reverse_lazy('person_details')

    def get_success_url(self, **kwargs):
        return reverse("person_details", kwargs={'pk': self.object.pk})


class PersonDetailView(DetailView):
    """Page with person's details """

    model = Person
    template_name = 'person_details.html'

    def get_context_data(self, **kwargs):
        """Insert the object into the context dict"""

        ctx = super().get_context_data(**kwargs)
        person = get_object_or_404(Person, pk=self.kwargs['pk'])
        try:
            movies = Movie.objects.filter(
                Q(director=person) |
                Q(screenplay=person) |
                Q(starring=person)).distinct()
            ctx["movies"] = movies
            return ctx
        except:
            return ctx


class PersonUpdateView(UpdateView):
    """Edit person's name and photo"""

    model = Person
    form_class = PersonForm
    template_name = 'person_edit.html'


class PersonDeleteView(DeleteView):
    """Delete person from DB"""

    model = Person
    template_name = 'del_person.html'
    success_url = reverse_lazy('stars_list')

    def get_context_data(self, **kwargs):
        person = get_object_or_404(Person, pk=self.kwargs['pk'])
        ctx = super().get_context_data(**kwargs)
        ctx['person'] = person
        return ctx
