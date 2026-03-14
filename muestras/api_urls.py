from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('muestras', views.MuestraViewSet)

urlpatterns = router.urls