from django.template.defaulttags import register
from django.views import generic
from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class IndexView(generic.TemplateView):
    template_name = 'dankswank/index.html'


# @register.filter
# def get_attr(obj, key):
#     return getattr(obj, key)


# class IndexView(generic.ListView):
#     template_name = 'movies/index.html'
#     context_object_name = 'movies'

#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
#         context.update({
#             'movie_attribute_names': Movie.get_movie_attribute_names(),
#             'movie_attribute_keys': Movie.get_movie_attribute_keys()
#         })
#         return context

#     def get_queryset(self):
#         return Movie.objects.order_by('college_release_date')


# class DetailView(generic.DetailView):
#     model = Movie
#     template_name = 'movies/detail.html'
