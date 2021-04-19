from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Genre, Movie, Person


def validate_rating(rating):
    """Check the rating length"""

    if len(str(rating)) != 2:
        raise ValidationError("{} rating is not valid!".format(rating))


def validate_year(year):
    """Check the year length"""

    if len(str(year)) != 4:
        raise ValidationError("{} year is not valid!".format(year))


class MovieForm(forms.ModelForm):
    """Form to create or update movie"""

    class Meta:
        """Class Meta"""
        model = Movie
        fields = ['title', 'director', 'screenplay', 'starring', 'year', 'rating', 'genre', 'image']

    def clean(self):
        """Check the year length"""
        cleaned_data = super().clean()
        if len(str(cleaned_data['year'])) < 4:
            raise ValidationError('Invalid year!')


class PersonForm(forms.ModelForm):
    """Form to create/update person"""

    class Meta:
        """Class Meta"""
        model = Person
        fields = ['first_name', 'last_name', 'image']


class SearchMovieForm(forms.Form):
    """Form to search a movie"""

    title = forms.CharField(
        label='Title: ',
        widget=forms.TextInput(),
        required=False
    )
    cast_name = forms.CharField(
        label='Cast name: ',
        widget=forms.TextInput(),
        required=False
    )
    year_from = forms.IntegerField(
        validators=[validate_year],
        required=False,
        min_value=0,
        max_value=datetime.now().year
    )
    year_to = forms.IntegerField(
        validators=[validate_year],
        required=False,
        min_value=0,
        max_value=datetime.now().year
    )
    rating_from = forms.FloatField(
        validators=[validate_rating],
        required=False,
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'step': "0.1"})
    )
    rating_to = forms.FloatField(
        validators=[validate_rating],
        required=False,
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'step': "0.1"})
    )
    genre = forms.ModelMultipleChoiceField(
        label='Genre: ',
        widget=forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
        queryset=Genre.objects.all(),
        required=False
    )


class SearchPersonForm(forms.Form):
    """Form to search a movie star"""

    search = forms.CharField(
        label='Search:',
        widget=forms.TextInput(attrs={'placeholder': 'search person...'})
    )

