from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'', views.MovieViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
