from rest_framework.routers import DefaultRouter

from .views_api import EmployeeViewSet

router = DefaultRouter()
router.register(
    'employees',
    EmployeeViewSet,
    basename='employee',
)

urlpatterns = router.urls