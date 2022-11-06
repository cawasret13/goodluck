from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from Calculations.views import LoadFile, selectionAnalogs, Calculation, ChangeCoef, CalculationsPool
from db.views import MetroView, RegionView
from personal_area.views import createUser, GetUser

router = SimpleRouter()

router.register('api/v1/metro', MetroView),
router.register('api/v1/region', RegionView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/calc', LoadFile.as_view()),
    path('api/v1/ref', selectionAnalogs.as_view()),
    path('api/v1/calc/report', Calculation.as_view()),
    path('api/v1/change/coefficient', ChangeCoef.as_view()),
    path('api/v1/calc/pool', CalculationsPool.as_view()),
    path('api/v1/user/register', createUser.as_view()),
    path('api/v1/user', GetUser.as_view()),

]
urlpatterns += router.urls
