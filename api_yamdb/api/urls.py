from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CreateUser, UserViewSet, get_jwt_token

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', CreateUser.as_view()),
    path('v1/auth/token/', get_jwt_token),
]
