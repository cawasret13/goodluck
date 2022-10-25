from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from Calculations.views import GetDataForm
from db.views import MetroView, RegionView

router = SimpleRouter()

router.register('api/v1/metro', MetroView)
router.register('api/v1/region', RegionView)
# router.register('api/v1/calculate', GetDataForm)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/calc', GetDataForm.as_view())
]
urlpatterns += router.urls
