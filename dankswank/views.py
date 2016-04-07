from django.views import generic
from movies.models import Movie
from dankswank.models import Dankswank
from datetime import datetime
import pytz


class IndexView(generic.ListView):
    template_name = 'dankswank/index.html'
    context_object_name = 'movies'

    def get_last_update(self):
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        last_update = Dankswank.get_last_update()
        if last_update == "never":
            return "unknown"
        else:
            return int((now - last_update).total_seconds() / 3600)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'movie_attributes': zip(Movie.get_movie_attribute_keys(), Movie.get_movie_attribute_names()),
            'movie_attribute_names': Movie.get_movie_attribute_names(),
            'movie_attribute_keys': Movie.get_movie_attribute_keys(),
            'last_update': self.get_last_update()
        })
        return context

    def get_queryset(self):
        return Movie.objects.order_by('college_release_date')
