from django.views import generic
from movies.models import Movie


class IndexView(generic.ListView):
    template_name = 'dankswank/index.html'
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'movie_attributes': zip(Movie.get_movie_attribute_keys(), Movie.get_movie_attribute_names()),
            'movie_attribute_names': Movie.get_movie_attribute_names(),
            'movie_attribute_keys': Movie.get_movie_attribute_keys()
        })
        return context

    def get_queryset(self):
        return Movie.objects.order_by('college_release_date')
