from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from db.views import MetroView, RegionView

router = SimpleRouter()

router.register('api/v1/metro', MetroView)
router.register('api/v1/region', RegionView)
urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
