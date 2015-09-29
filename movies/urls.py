from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter
from movies.management.commands.getmovies import Command as MovieCollectorCommand
import sched, time, thread


router = SimpleRouter()
router.register(r'', views.MovieViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]


def get_movies(sc):
    mcc = MovieCollectorCommand()
    mcc.populate_movie_database(True)

    sc.enter(28800, 1, get_movies, (sc,))

 
def start_getting_movies():
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(1, 1, get_movies, (scheduler,))
    scheduler.run()
 
thread.start_new_thread(start_getting_movies, ())

print 'hello'
