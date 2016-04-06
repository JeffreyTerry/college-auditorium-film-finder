from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter
from movies.management.commands.getmovies import Command as MovieCollectorCommand
from movies.management.commands.prunemovies import Command as MoviePrunerCommand
from dankswank.models import Dankswank
import sched, time, thread
import logging
import os


router = SimpleRouter()
router.register(r'', views.MovieViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]

logger = logging.getLogger(__name__)


def get_movies(sc):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logfile = os.path.join(BASE_DIR, 'debug.log')

    # Empty the log file
    with open(logfile, 'w') as f:
        f.write('')

    logger.info('---------------------------')
    logger.info(' Getting movie information ')
    logger.info('---------------------------')

    mcc = MovieCollectorCommand()
    mcc.populate_movie_database(True)

    mpc = MoviePrunerCommand()
    mpc.prune_movie_database()

    sc.enter(28800, 1, get_movies, (sc,))


def start_getting_movies():
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(1, 1, get_movies, (scheduler,))
    scheduler.run()

thread.start_new_thread(start_getting_movies, ())
